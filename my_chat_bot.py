import discord
from google import genai
from google.genai.errors import APIError  # InternalServerError를 제거하고 APIError만 사용
import os
import asyncio  # 비동기 대기를 위한 임포트

# ================================
#  환경 변수 불러오기
# ================================
try:
    # 환경 변수는 사용자 시스템에서 불러오므로, 코드는 그대로 유지합니다.
    DISCORD_TOKEN = os.environ['MY_DISCORD_TOKEN']
    GEMINI_API_KEY = os.environ['MY_GEMINI_KEY']
except KeyError:
    print("🚨 환경 변수 'MY_DISCORD_TOKEN' 또는 'MY_GEMINI_KEY'를 파이참 설정에 추가해 주세요.")
    exit()

# ================================
#  Gemini 클라이언트 초기화
# ================================
try:
    client_gemini = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"Gemini 클라이언트 초기화 오류: {e}")
    exit()

# ================================
#  디스코드 봇 설정
# ================================
intents = discord.Intents.default()
intents.message_content = True
client_discord = discord.Client(intents=intents)


# ================================
#  긴 메시지를 2000자씩 분할하는 함수
# ================================
def split_message(text, limit=2000):
    """디스코드의 2000자 제한을 피하기 위해 자동으로 분할."""
    return [text[i:i + limit] for i in range(0, len(text), limit)]


# ================================
#  [개선] 지수 백오프 재시도 로직 함수
# ================================
MAX_RETRIES = 10  # 최대 재시도 횟수를 10회로 설정
INITIAL_DELAY = 1  # 1초부터 시작


async def generate_content_with_retry(model_name: str, contents: str, thinking_message: discord.Message):
    """
    지수 백오프를 사용하여 Gemini API 호출을 재시도합니다.
    500번대 오류(APIError로 포괄 처리) 발생 시 유용합니다.
    """
    delay = INITIAL_DELAY

    # 모델명은 'gemini-2.5-flash'로 고정
    model = model_name

    for attempt in range(MAX_RETRIES):
        try:
            # 1. API 호출 시도
            response = client_gemini.models.generate_content(
                model=model,
                contents=contents
            )
            print(f"✅ 캬루쨩이 프로그램을 가동중입니다!! API 호출 성공 (시도 {attempt + 1}회)")
            return response

        except APIError as e:  # InternalServerError 제거, APIError로 503 포함 모든 API 오류를 잡음
            # 2. 서버 오류 또는 API 오류 처리 (503 오류가 여기에 해당됨)
            print(f"⚠️ Gemini API 일시적 오류 발생 (시도 {attempt + 1}/{MAX_RETRIES}회): {e}")

            if attempt < MAX_RETRIES - 1:
                # 3. 재시도 전에 사용자에게 알림 및 대기
                await thinking_message.edit(
                    content=f'⚠️ 캬루쨩이 생각을 깊게 하고 있어요..! {delay}초 후 자동으로 다시 시도합니다... (재시도 {attempt + 2}/{MAX_RETRIES}회)'
                )
                await asyncio.sleep(delay)
                delay *= 2  # 지수 백오프: 대기 시간을 2배로 증가

            else:
                # 4. 최대 재시도 횟수 초과
                raise Exception(f"최대 재시도 횟수({MAX_RETRIES}회) 초과. 최종 API 응답 실패.") from e

    # 모든 재시도 실패 시 None 반환 (실제로는 위의 Exception이 발생할 것임)
    return None


# ================================
#  봇 이벤트
# ================================
@client_discord.event
async def on_ready():
    print(f'로그인 성공! 봇 이름: {client_discord.user}')


@client_discord.event
async def on_message(message):
    if message.author == client_discord.user:
        return

    if message.content.startswith('!캬루야 '):
        user_question = message.content[5:].strip()

        thinking_message = await message.channel.send('💭 캬루쨩이 답변을 생각 중입니다...')

        try:
            # [개선 적용] 재시도 로직이 포함된 함수 호출
            response = await generate_content_with_retry(
                model_name='gemini-2.5-flash',
                contents=user_question,
                thinking_message=thinking_message
            )

            # 응답이 없거나 내용이 비어있으면 오류 처리
            if not response or not (hasattr(response, "text") and response.text):
                await thinking_message.edit(
                    content="🚫 캬루쨩으로부터 빈 응답을 받았습니다. 질문을 다시 확인해주세요."
                )
                return

            answer = response.text

            # 디스코드에 보내는 전체 메시지 생성
            full_message = (
                f'**{message.author.display_name}님의 질문:** {user_question}\n\n'
                f'**🤖 답변:**\n{answer}'
            )

            # 2000자 단위로 분할
            parts = split_message(full_message)

            # 첫 메시지는 edit()
            await thinking_message.edit(content=parts[0])

            # 나머지는 새로운 메시지로 전송
            for part in parts[1:]:
                await message.channel.send(part)

        except Exception as e:
            # 최종 실패 시 사용자에게 오류 메시지 전달
            await thinking_message.edit(
                content=f"죄송해요! 캬루쨩의 API 호출 중 복구 불가능한 오류가 발생했습니다.\n오류: `{e}`"
            )


# ================================
#  봇 실행
# ================================
client_discord.run(DISCORD_TOKEN)