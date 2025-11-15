import os
import subprocess
import sys
import random

video_folder = 'videos'
output_filename = 'merged_video_ffmpeg_shuffled.mp4'

video_files = []
for filename in os.listdir(video_folder):
    if filename.endswith(('.mp4', '.mov', '.avi', '.mkv')):
        video_files.append(os.path.join(video_folder, filename))

if not video_files:
    print(f"경고: '{video_folder}' 폴더에 합칠 동영상 파일이 없습니다.")
    sys.exit()

# 셔플 여부 설정 (디폴트: True)
shuffle_videos = True

if shuffle_videos:
    random.shuffle(video_files)
else:
    # 셔플하지 않음
    pass

print("✅ 파일 목록:")
for file in video_files:
    print(f"- {os.path.basename(file)}")

list_file_path = os.path.join(os.getcwd(), 'file_list_temp.txt')
with open(list_file_path, 'w', encoding='utf-8') as f:
    for file in video_files:
        f.write(f"file '{file.replace(os.path.sep, '/')}'\n")

print(f"\n🚀 동영상 합치기 시작! (FFmpeg 실행 중...)")

try:
    command = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', list_file_path,
        '-c', 'copy',
        output_filename
    ]

    subprocess.run(command, check=True)

    print(f"\n🎉 모든 동영상이 성공적으로 '{output_filename}' 파일로 합쳐졌습니다!")

except subprocess.CalledProcessError as e:
    print(f"\n❌ FFmpeg 실행 중 오류 발생. 코드가 {e.returncode}로 종료되었습니다.")
    print("원인: FFmpeg 실행 파일이 PATH에 없거나, 동영상 파일에 문제가 있을 수 있습니다.")
except FileNotFoundError:
    print("\n❌ 오류: 'ffmpeg' 실행 파일을 찾을 수 없습니다. 경로를 확인해 주세요.")

os.remove(list_file_path)
