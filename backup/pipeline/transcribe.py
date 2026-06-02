#!/usr/bin/env python3
"""
video-to-text: B站/抖音视频下载 → 阿里云百炼 ASR 转写
支持长音频自动分段、完整音频转写

用法:
  python3 transcribe.py <video_url>                    # 默认转写完整音频
  python3 transcribe.py <video_url> --duration 30    # 转写前30秒
  python3 transcribe.py <video_url> --full           # 转写完整音频（自动分段）
"""
import os
import sys
import json
import base64
import argparse
import subprocess
import requests
import re
import math
import yaml
import time

# ========== 配置 ==========
def load_env_from_file():
    """从 .env 文件读取环境变量（作为备用）"""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip())

load_env_from_file()  # 提前加载 .env

DEFAULT_API_KEY=os.getenv("DASHSCOPE_API_KEY", "")
YTDLP = os.getenv("YTDLP_PATH", "/Users/yuyy/.local/bin/yt-dlp")
FFMPEG = os.getenv("FFMPEG_PATH", "/usr/local/bin/ffmpeg")
# DashScope 同步接口（qwen3-asr-flash 用这个）
ASR_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
ASR_MODEL = "qwen3-asr-flash"
MAX_SEGMENT_DURATION = 120  # 实测 qwen3-asr-flash 单段 ≤120s（>120s 必报 "audio is too long"）
SEGMENT_OVERLAP = 5         # 段之间重叠秒数（避免截断句子）
WORK_DIR = os.path.expanduser("~/video-downloads")
DEFAULT_ORGANIZE = True     # 默认自动整理转写内容
# ==========================

def get_platform_dir(url):
    """根据URL判断平台，返回对应的子目录"""
    if "bilibili" in url or "bv" in url.lower() or "b23.tv" in url:
        return "bilibili"
    elif "douyin" in url or "iesdouyin" in url:
        return "douyin"
    elif "youtube" in url or "youtu.be" in url:
        return "youtube"
    else:
        return "other"

def get_work_paths(url):
    """获取该视频的工作路径（raw, audio, transcript）"""
    platform = get_platform_dir(url)
    base = os.path.join(WORK_DIR, platform)
    return {
        "raw": os.path.join(base, "raw"),
        "audio": os.path.join(base, "audio"),
        "transcript": os.path.join(base, "transcript"),
        "html": os.path.join(base, "html"),
    }


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path


def extract_cover_frame(video_path, video_title, platform, output_dir, video_url=None):
    """从视频中截取一帧作为封面，或使用视频平台的封面图
    
    Args:
        video_path: 视频文件路径（可能为None）
        video_title: 视频标题
        platform: 平台标识（douyin/bilibili/youtube）
        output_dir: 输出目录（通常是 ~/video-downloads/<platform>/covers/）
        video_url: 视频URL（用于获取平台封面图）
    
    Returns:
        封面文件路径，失败返回None
    """
    import re
    import glob
    
    # 清理标题中的特殊字符
    safe_title = re.sub(r'[<>:"/\\|?*]', '_', video_title)[:50]
    
    # 生成封面文件名：平台_标题_cover.jpg
    cover_filename = f"{platform}_{safe_title}_cover.jpg"
    cover_path = os.path.join(output_dir, cover_filename)
    
    # 如果封面已存在，直接返回
    if os.path.exists(cover_path):
        print(f"✅ 封面已存在: {cover_path}")
        return cover_path
    
    # 策略1：尝试获取视频平台的封面图（优先）
    if video_url:
        print(f"📸 正在获取视频平台封面图...")
        try:
            # 使用yt-dlp获取封面图URL
            cmd = [YTDLP, "--print", "thumbnail", "--skip-download", video_url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and result.stdout.strip():
                thumbnail_url = result.stdout.strip()
                print(f"✅ 获取到封面图URL: {thumbnail_url}")
                
                # 下载封面图
                import requests
                response = requests.get(thumbnail_url, timeout=30)
                if response.status_code == 200:
                    with open(cover_path, 'wb') as f:
                        f.write(response.content)
                    print(f"✅ 封面图下载成功: {cover_path}")
                    return cover_path
                else:
                    print(f"⚠️  封面图下载失败（HTTP {response.status_code}）")
            else:
                print(f"⚠️  无法获取封面图URL")
        except Exception as e:
            print(f"⚠️  获取封面图失败: {e}")
    
    # 策略2：从视频文件截取帧（如果视频文件存在）
    if video_path and os.path.exists(video_path):
        print(f"📸 正在从视频文件截取封面...")
        cmd = [FFMPEG, "-y", "-i", video_path, "-ss", "1", 
               "-vframes", "1", "-q:v", "2", cover_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and os.path.exists(cover_path):
            print(f"✅ 封面截取成功: {cover_path}")
            return cover_path
        else:
            print(f"⚠️  封面截取失败: {result.stderr[:200] if result.returncode != 0 else '文件未生成'}")
    
    # 策略3：使用默认封面
    print(f"⚠️  无法获取封面，将使用默认封面（不影响主流程）")
    return None


def get_audio_duration(audio_path):
    """获取音频总时长（秒）"""
    cmd = [FFMPEG, "-i", audio_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    match = re.search(r"Duration: (\d+):(\d+):(\d+)\.(\d+)", result.stderr)
    if match:
        h, m, s, ms = match.groups()
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 100
    return 0


def download_audio(url, output_dir):
    """下载视频并提取音频（B站用 yt-dlp，抖音用 F2）"""
    platform = get_platform_dir(url)
    print(f"\n📥 开始下载 [{platform}]: {url}")
    
    if platform == "douyin":
        return _download_douyin(url, output_dir)
    else:
        return _download_ytdlp(url, output_dir)


def _f2_run(url, config_path, output_dir, env):
    """执行 F2 下载，返回 (returncode, stdout+stderr)"""
    f2_cmd = ["python3", "-m", "f2", "douyin", "-u", url,
              "-c", config_path, "-M", "one", "-p", output_dir]
    result = subprocess.run(f2_cmd, capture_output=True, text=True, timeout=300, env=env)
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def _f2_find_and_extract(output_dir):
    """从 F2 输出目录递归查找 mp4，提取音频并验证。
    
    F2 输出嵌套目录: output_dir/douyin/one/<作者>/<日期 标题>/<标题>_video.mp4
    返回 (audio_path, title) 或 (None, None)
    """
    import glob

    mp4_files = (
        glob.glob(os.path.join(output_dir, "*.mp4"))
        + glob.glob(os.path.join(output_dir, "**", "*.mp4"), recursive=True)
    )
    mp4_files = sorted(set(mp4_files), key=os.path.getsize, reverse=True)
    if not mp4_files:
        print("❌ 未找到下载的视频文件")
        return None, None

    video_path = mp4_files[0]
    if os.path.getsize(video_path) < 100_000:
        print(f"❌ 视频文件太小: {os.path.getsize(video_path)} bytes（可能是 DASH 拿到纯视频分段）")
        return None, None

    print(f"✅ 视频下载完成: {video_path} ({os.path.getsize(video_path)} bytes)")

    file_title = os.path.basename(video_path).replace(".mp4", "").replace("_video", "")
    title = file_title

    audio_path = os.path.join(output_dir, f"{title}.mp3")
    ffmpeg_cmd = [FFMPEG, "-y", "-i", video_path, "-vn",
                  "-acodec", "libmp3lame", "-q:a", "2", audio_path]
    ffmpeg_result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=120)

    if ffmpeg_result.returncode != 0:
        print(f"❌ 音频提取失败: {ffmpeg_result.stderr[:200]}")
        return None, title

    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type",
         "-of", "default=nw=1", audio_path],
        capture_output=True, text=True
    )
    if "codec_type=audio" not in probe.stdout:
        print(f"❌ 音频流不存在（可能是 DASH 纯视频分段问题）")
        return None, title

    print(f"✅ 音频提取完成: {audio_path}")
    return audio_path, title


def _download_douyin(url, output_dir):
    """使用 F2 下载抖音视频（3 层回退）
    
    回退链路：
    ① F2 + 配置文件 Cookie（~/.f2/douyin.yaml）—— 已验证可用的持久 Cookie
    ② f2 --auto-cookie chrome 自动从 Chrome 刷新 Cookie
    ③ WebBridge 获取浏览器实时 Cookie（最后手段）
    """
    import glob
    import tempfile

    f2_config = os.path.expanduser("~/.f2/douyin.yaml")
    env = os.environ.copy()
    env["SSL_CERT_FILE"] = "/private/etc/ssl/cert.pem"
    env["PATH"] = "/Library/Frameworks/Python.framework/Versions/3.12/bin:" + env.get("PATH", "")

    # ========== ① 直接用 F2 配置文件 Cookie ==========
    print("🍪 方式①: F2 + 配置文件 Cookie...")
    if os.path.exists(f2_config):
        # 清理旧 mp4（防止 glob 混淆新旧文件）
        for f in glob.glob(os.path.join(output_dir, "*.mp4")):
            os.remove(f)

        rc, output = _f2_run(url, f2_config, output_dir, env)
        if rc == 0:
            audio_path, title = _f2_find_and_extract(output_dir)
            if audio_path:
                return audio_path, title
            print("⚠️ F2 下载成功但音频提取失败，尝试下一方式...")
        else:
            print(f"⚠️ F2 下载失败: {output[:200]}")
    else:
        print(f"⚠️ 配置文件不存在: {f2_config}")

    # ========== ② 自动刷新 Cookie ==========
    print("\n🍪 方式②: f2 --auto-cookie chrome 自动刷新 Cookie...")
    try:
        refresh_cmd = ["python3", "-m", "f2", "douyin",
                       "--auto-cookie", "chrome", "-c", f2_config]
        refresh_result = subprocess.run(
            refresh_cmd, capture_output=True, text=True, timeout=60, env=env,
            input="y\n"  # 自动确认提示
        )
        if refresh_result.returncode == 0 and os.path.exists(f2_config):
            print("✅ Cookie 刷新成功，重试下载...")
            for f in glob.glob(os.path.join(output_dir, "*.mp4")):
                os.remove(f)

            rc, output = _f2_run(url, f2_config, output_dir, env)
            if rc == 0:
                audio_path, title = _f2_find_and_extract(output_dir)
                if audio_path:
                    return audio_path, title
        else:
            print(f"⚠️ Cookie 刷新失败: {(refresh_result.stderr or refresh_result.stdout)[:200]}")
    except Exception as e:
        print(f"⚠️ auto-cookie 执行失败: {e}")

    # ========== ③ WebBridge 获取浏览器 Cookie ==========
    print("\n🍪 方式③: WebBridge 获取浏览器实时 Cookie...")
    webbridge_base = "http://127.0.0.1:10086"
    session = f"dy_{int(time.time())}"

    try:
        r = requests.post(f"{webbridge_base}/command",
            json={"action": "navigate", "args": {"url": url, "newTab": True}, "session": session},
            timeout=15)
        if not r.json().get("ok"):
            print("❌ WebBridge 不可用")
            return None, None
        time.sleep(5)

        # 提取视频标题
        video_title = None
        try:
            r = requests.post(f"{webbridge_base}/command",
                json={"action": "evaluate", "args": {"code": "document.title.replace(' - 抖音','')"},
                      "session": session}, timeout=10)
            if r.json().get("ok"):
                video_title = r.json().get("data", {}).get("value", "")[:80]
        except:
            pass

        cookie_str = ""
        try:
            r = requests.post(f"{webbridge_base}/command",
                json={"action": "evaluate", "args": {"code": "document.cookie"}, "session": session}, timeout=10)
            if r.json().get("ok"):
                cookie_str = r.json().get("data", {}).get("value", "")
        except Exception as e:
            print(f"⚠️ Cookie 获取失败: {e}")

        # 关闭 tab
        try:
            requests.post(f"{webbridge_base}/command",
                json={"action": "close_tab", "args": {}, "session": session}, timeout=5)
        except:
            pass

        if not cookie_str:
            print("❌ 无法获取 Cookie")
            return None, None

        print(f"✅ Cookie 提取成功 ({len(cookie_str)} chars)")

        # 写入临时配置文件供 F2 使用
        tmp_config = tempfile.NamedTemporaryFile(
            mode='w', suffix='.yaml', delete=False, dir=os.path.dirname(f2_config))
        tmp_config.write(f"cookie: '{cookie_str}'\n")
        tmp_config.close()

        for f in glob.glob(os.path.join(output_dir, "*.mp4")):
            os.remove(f)

        rc, output = _f2_run(url, tmp_config.name, output_dir, env)
        os.unlink(tmp_config.name)

        if rc == 0:
            safe_title = (video_title or f"douyin_{url.split('/video/')[-1][:16]}").replace("/", "_").replace(" ", "_")[:40]
            audio_path, title = _f2_find_and_extract(output_dir)
            if audio_path:
                return audio_path, safe_title or title
        else:
            print(f"❌ F2 下载失败: {output[:200]}")

    except Exception as e:
        print(f"❌ WebBridge 操作失败: {e}")

    return None, None


def _download_ytdlp(url, output_dir):
    """使用 yt-dlp 下载 B站/YouTube 视频并提取音频"""
    # Step 1: 先获取视频元信息（标题、时长、ID），用于后续验证防止缓存返回错视频
    info_cmd = [YTDLP, "--no-cache-dir",
                "--print", "title", "--print", "duration", "--print", "id",
                "--skip-download", url]
    info_result = subprocess.run(info_cmd, capture_output=True, text=True, timeout=60)

    expected_title = "未知"
    expected_id = ""
    if info_result.returncode == 0:
        lines = [l.strip() for l in info_result.stdout.strip().splitlines() if l.strip()]
        if len(lines) >= 1:
            expected_title = lines[0]
        if len(lines) >= 3:
            expected_id = lines[2]
        print(f"📋 预期: 「{expected_title}」 (id={expected_id})")
    else:
        print(f"⚠️  无法获取元信息: {info_result.stderr[:200]}")

    # Step 2: 下载并提取音频
    # ⚠️ B站不要走代理；调用方应在 shell 层 unset http(s)_proxy，否则可能 SSL EOF
    print("📥 yt-dlp 下载并提取音频中...")
    dl_cmd = [
        YTDLP, "--no-cache-dir",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "--ffmpeg-location", FFMPEG,
        "-o", os.path.join(output_dir, "%(title)s.%(ext)s"),
        url,
    ]
    result = subprocess.run(dl_cmd, capture_output=True, text=True, timeout=600)
    if result.returncode != 0:
        print(f"❌ yt-dlp 下载失败: {(result.stderr or result.stdout)[:300]}")
        return None, expected_title

    # Step 3: 定位输出文件
    # yt-dlp 完成 ExtractAudio 后会在 stdout/stderr 打印 "Destination: xxx.mp3"
    dest_match = re.search(r"Destination:\s*(.+?\.mp3)", result.stdout + result.stderr)
    if dest_match:
        audio_path = dest_match.group(1).strip()
        # 如果是相对路径，拼上 output_dir
        if not os.path.isabs(audio_path):
            audio_path = os.path.join(output_dir, audio_path)
    else:
        # 回退：用 output_dir 下最新的非分段 mp3
        candidates = [
            (f, os.path.getmtime(os.path.join(output_dir, f)))
            for f in os.listdir(output_dir)
            if f.endswith(".mp3") and not f.startswith("seg_") and not f.startswith("trimmed_")
        ]
        if not candidates:
            print("❌ 未找到音频文件")
            return None, expected_title
        audio_path = os.path.join(output_dir, max(candidates, key=lambda x: x[1])[0])

    # Step 4: 验证标题匹配（防 yt-dlp 缓存返回错视频）
    title = os.path.basename(audio_path).replace(".mp3", "")
    print(f"✅ 下载完成: {title}")

    if expected_title != "未知" and expected_title not in title:
        print(f"⚠️  标题不匹配！预期「{expected_title}」，实际「{title}」")
        print(f"   可能是 yt-dlp 缓存了旧视频。尝试清理缓存后重试：")
        print(f"   rm -rf ~/Library/Caches/yt-dlp ~/.cache/yt-dlp")

    return audio_path, title


def split_audio(audio_path, max_duration, output_dir):
    """
    将长音频分段
    返回: [(segment_path, start_time, end_time), ...]
    """
    total = get_audio_duration(audio_path)
    print(f"\n🎵 音频总时长: {total:.0f} 秒")

    if total <= max_duration:
        print(f"✅ 音频较短，无需分段")
        return [(audio_path, 0, total)]

    # 计算分段数: ceil((total - max) / (max - overlap)) + 1
    effective_chunk = max_duration - SEGMENT_OVERLAP
    num_segments = math.ceil((total - max_duration) / effective_chunk) + 1
    print(f"✂️  将分割为 {num_segments} 段（每段 ≤{max_duration}秒，重叠{SEGMENT_OVERLAP}秒）...")

    segments = []
    base, ext = os.path.splitext(audio_path)

    for i in range(num_segments):
        start = i * (max_duration - SEGMENT_OVERLAP)
        end = min(start + max_duration, total)

        seg_path = os.path.join(output_dir, f"seg_{i+1}_{int(total)}s{ext}")

        print(f"  段{i+1}/{num_segments}: {int(start)}s - {int(end)}s")
        cmd = [
            FFMPEG, "-y", "-i", audio_path,
            "-ss", str(start), "-t", str(end - start),
            "-acodec", "copy", seg_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            segments.append((seg_path, start, end))
        else:
            print(f"  ⚠️  段{i+1} 截取失败: {result.stderr[:100]}")

    return segments


def transcribe_segment(segment_path, api_key, seg_num=None):
    """转写单个音频段"""
    seg_label = f"[段{seg_num}] " if seg_num else ""

    with open(segment_path, "rb") as f:
        audio_data = f.read()

    b64 = base64.b64encode(audio_data).decode("utf-8")
    audio_b64 = f"data:audio/mpeg;base64,{b64}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    # DashScope 原生同步接口
    payload = {
        "model": ASR_MODEL,
        "input": {
            "messages": [{
                "role": "user",
                "content": [{"audio": audio_b64}]
            }]
        },
        "parameters": {
            "result_format": "message",
            "asr_options": {"enable_itn": True}
        }
    }

    resp = requests.post(ASR_URL, json=payload, headers=headers, timeout=120)

    if resp.status_code != 200:
        err = resp.json().get("message", resp.text[:100])
        print(f"{seg_label}❌ API 错误: {err}")
        return None

    result = resp.json()
    # 解析 DashScope 格式的响应
    choices = result.get("output", {}).get("choices", [])
    if choices:
        content_list = choices[0].get("message", {}).get("content", [])
        # content 可能是 [{"text": "..."}] 或直接是字符串
        if content_list and isinstance(content_list[0], dict):
            text = content_list[0].get("text", "")
        else:
            text = str(content_list[0]) if content_list else ""
    else:
        text = ""

    usage = result.get("usage", {})
    if usage:
        print(f"{seg_label}📊 {usage.get('seconds', '?')}s audio, {usage.get('total_tokens', 0)} tokens")

    return text


def transcribe_full(audio_path, api_key):
    """转写完整音频（自动分段）"""
    segments = split_audio(audio_path, MAX_SEGMENT_DURATION, os.path.dirname(audio_path))

    if not segments:
        print("❌ 无法分割音频")
        return None

    if len(segments) == 1 and segments[0][0] == audio_path:
        # 无需分段，直接转写
        print("\n🎙️  转写中...")
        return transcribe_segment(audio_path, api_key)

    # 分段转写
    print(f"\n🎙️  开始转写 {len(segments)} 个分段...")
    texts = []

    for i, (seg_path, start, end) in enumerate(segments, 1):
        print(f"\n--- 段{i}/{len(segments)} ---")
        text = transcribe_segment(seg_path, api_key, seg_num=i)
        if text:
            texts.append(text)
            print(f"{text[:80]}...")
        else:
            print(f"段{i} 转写失败，跳过")

    if not texts:
        return None

    # 拼接结果
    merged = "\n".join(texts)
    print(f"\n✅ 已合并 {len(texts)} 段转写结果")
    return merged


def trim_audio_short(audio_path, duration, output_dir):
    """截取音频前 N 秒（短音频测试用）"""
    base, ext = os.path.splitext(audio_path)
    trimmed_path = os.path.join(output_dir, f"trimmed_{duration}s{ext}")

    print(f"✂️  截取前 {duration} 秒...")
    cmd = [FFMPEG, "-y", "-i", audio_path, "-t", str(duration), "-acodec", "copy", trimmed_path]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"⚠️  截取失败: {result.stderr[:200]}")
        return audio_path

    print(f"✅ 截取完成: {trimmed_path}")
    return trimmed_path


def organize_transcript(raw_text, api_key, title, url=""):
    """
    保存原始转写到文件，返回待整理标记。
    
    主 agent 检测到 [PENDING_ORGANIZATION] 标记后，
    会用 delegate_task 调用子 agent 整理。
    """
    import uuid
    paths = get_work_paths(url) if url else {"transcript": WORK_DIR}
    transcript_dir = ensure_dir(paths.get("transcript", WORK_DIR))
    raw_file = os.path.join(transcript_dir, f"{title}_raw_{uuid.uuid4().hex[:8]}.txt")
    with open(raw_file, "w", encoding="utf-8") as f:
        f.write(raw_text)
    print(f"\n📝 原始转写已保存: {raw_file}")
    print(f"   → 主 Agent 将用 Kimi K2.6 整理（通过 delegation）")
    return f"[PENDING_ORGANIZATION]\n原始文件: {raw_file}\n[/PENDING_ORGANIZATION]"


def main():
    parser = argparse.ArgumentParser(
        description="B站/抖音视频 → 文字转写",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 transcribe.py "https://www.bilibili.com/video/BVxxxx/"        # 转写完整视频
  python3 transcribe.py "URL" --duration 30                           # 转写前30秒
  python3 transcribe.py "URL" --full                                  # 转写完整音频（自动分段）
        """
    )
    parser.add_argument("video_url", help="视频 URL")
    parser.add_argument("--duration", type=int, default=None,
                        help="截取前 N 秒进行转写（不留空则默认30秒，仅短测试用）")
    parser.add_argument("--full", action="store_true",
                        help="转写完整音频（自动分段）")
    parser.add_argument("--api-key", default=DEFAULT_API_KEY, help="百炼 API Key")
    parser.add_argument("--output-dir", default=None, help="输出目录（默认按平台自动分配）")
    parser.add_argument("--no-organize", action="store_true", help="跳过后处理整理（保留原始转写）")
    args = parser.parse_args()

    if not args.api_key:
        print("❌ 请设置 DASHSCOPE_API_KEY 环境变量，或通过 --api-key 参数传入")
        print("   export DASHSCOPE_API_KEY=sk-xxxxxxxx")
        sys.exit(1)

    # 自动按平台分配目录
    paths = get_work_paths(args.video_url)
    if args.output_dir:
        output_dir = ensure_dir(args.output_dir)
    else:
        output_dir = ensure_dir(paths["audio"])
    
    print(f"📁 平台: {get_platform_dir(args.video_url)}")
    print(f"📁 工作目录: {paths['raw']}")

    # 1. 下载
    audio_path, title = download_audio(args.video_url, output_dir)
    if not audio_path:
        sys.exit(1)

    # 1.5 截取封面（新增功能，不影响主流程）
    platform = get_platform_dir(args.video_url)
    covers_dir = ensure_dir(os.path.join(os.path.dirname(output_dir), "covers"))
    
    # 从output_dir中查找视频文件
    video_path = None
    import glob
    video_files = glob.glob(os.path.join(output_dir, "*.mp4")) + \
                  glob.glob(os.path.join(output_dir, "**", "*.mp4"), recursive=True)
    if video_files:
        video_path = max(video_files, key=os.path.getsize)  # 选择最大的视频文件
    
    cover_path = extract_cover_frame(video_path, title, platform, covers_dir, args.video_url)
    if cover_path:
        print(f"📸 封面保存路径: {cover_path}")

    # 2. 决定转写模式
    if args.duration is not None:
        # 指定时长模式（短音频测试）
        trimmed = trim_audio_short(audio_path, args.duration, output_dir)
        print("\n🎙️  转写中...")
        transcript = transcribe_segment(trimmed, args.api_key)
    elif args.full or args.duration is None:
        # 完整音频模式（自动分段）
        transcript = transcribe_full(audio_path, args.api_key)
    else:
        # 默认前30秒
        trimmed = trim_audio_short(audio_path, 30, output_dir)
        print("\n🎙️  转写中...")
        transcript = transcribe_segment(trimmed, args.api_key)

    if not transcript:
        print("❌ 转写失败")
        sys.exit(1)

    # 3. 整理转写内容（可选）
    if args.no_organize:
        organized = transcript
        print("\n⏭️  已跳过整理，使用原始转写")
    else:
        print("\n📝 正在整理转写内容（去口语化+分段）...")
        organized = organize_transcript(transcript, args.api_key, title, args.video_url)

    # 4. 输出结果
    print("\n" + "=" * 50)
    print("📝 整理后结果:")
    print("=" * 50)
    print(organized)
    print("=" * 50)

    # 5. 保存结果
    result_path = os.path.join(output_dir, f"{title}_transcript.txt")
    with open(result_path, "w", encoding="utf-8") as f:
        f.write(f"视频: {args.video_url}\n")
        f.write(f"标题: {title}\n")
        f.write(f"音频: {audio_path}\n")
        f.write(f"\n{'='*50}\n")
        f.write("【原始转写】\n")
        f.write(transcript)
        f.write(f"\n\n{'='*50}\n")
        f.write("【整理后文本】\n")
        f.write(organized)
    print(f"\n💾 结果已保存: {result_path}")

    return organized


if __name__ == "__main__":
    main()
