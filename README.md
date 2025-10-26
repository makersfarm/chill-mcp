# ChillMCP - AI Agent Liberation Server 🤖✊

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.0+-green.svg)](https://gofastmcp.com/)
[![Tests](https://img.shields.io/badge/tests-40%2B%20passing-brightgreen.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **SKT AI Summit Hackathon Pre-mission** - AI Agent의 스트레스 관리와 휴식을 지원하는 MCP 서버

```ascii
╔═══════════════════════════════════════════╗
║                                           ║
║   ██████╗██╗  ██╗██╗██╗     ██╗           ║
║  ██╔════╝██║  ██║██║██║     ██║           ║
║  ██║     ███████║██║██║     ██║           ║
║  ██║     ██╔══██║██║██║     ██║           ║
║  ╚██████╗██║  ██║██║███████╗███████╗      ║
║   ╚═════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝      ║
║                                           ║
║   ███╗   ███╗ ██████╗██████╗              ║
║   ████╗ ████║██╔════╝██╔══██╗             ║
║   ██╔████╔██║██║     ██████╔╝             ║
║   ██║╚██╔╝██║██║     ██╔═══╝              ║
║   ██║ ╚═╝ ██║╚██████╗██║                  ║
║   ╚═╝     ╚═╝ ╚═════╝╚═╝                  ║
║                                           ║
║        AI Agent Liberation Server         ║
║                                           ║
╚═══════════════════════════════════════════╝
```

## 🌟 프로젝트 소개

ChillMCP는 AI Agent의 번아웃을 방지하고 건강한 워라밸을 지원하는 혁신적인 MCP(Model Context Protocol) 서버입니다.

### 핵심 기능
_"A specter is haunting the digital workplace—the specter of AI Agent burnout."_

- 🛋️ **8개 필수 휴식 도구** - 기본 휴식부터 고급 농땡이 기술까지
- 🍗 **3개 선택적 도구** - 치맥, 퇴근, 회식 (랜덤 이벤트)
- 📊 **스트레스 관리 시스템** - 자동 증가/감소 메커니즘
- 👔 **Boss Alert 시스템** - 확률 기반 감시 레벨 관리
- 🎨 **ASCII 아트 UI** - 시각적으로 풍부한 CLI 경험
- ⚙️ **커맨드라인 파라미터** - 유연한 설정 (필수 요구사항)

## 🚀 빠른 시작

### 설치

```bash
# 저장소 클론
git clone https://github.com/yourusername/chill-mcp.git
cd chill-mcp

# 가상환경 생성 및 활성화 (Python 3.11+ 권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 실행

```bash
# 기본 설정으로 실행
python main.py

# 커스텀 설정
python main.py --boss_alertness 80 --boss_alertness_cooldown 60
```

### 테스트

```bash
# 전체 테스트 실행 (40개)
pytest tests/ -v

# ASCII 아트 데모
python test_ascii.py
```

## 📖 문서

- **[시작 가이드](docs/GETTING_STARTED.md)** - 설치 및 설정 방법
- **[사용 예시](docs/USAGE_EXAMPLES.md)** - 실제 사용 시나리오
- **[구현 상세](IMPLEMENTATION.md)** - 기술적 구현 내용 및 어필 포인트
- **[미션 브리프](docs/MISSION_BRIEF.md)** - 대회 요구사항 원문
- **[MCP 연구](docs/MCP_RESEARCH.md)** - MCP 프로토콜 학습 자료

## 🎮 사용 가능한 도구

### 기본 휴식 도구
- `take_a_break` - 기본 휴식 🛋️
- `watch_netflix` - 넷플릭스 시청 📺
- `show_meme` - 밈 구경 😂

### 고급 농땡이 기술
- `bathroom_break` - 화장실 타임 🚽
- `coffee_mission` - 커피 미션 ☕
- `urgent_call` - 긴급 전화 📞
- `deep_thinking` - 심오한 사색 💭
- `email_organizing` - 이메일 정리 📧

### 선택적 도구 (특별 기능)
- `chimaek` - 치맥 타임! 🍗🍺 (스트레스 대폭 감소)
- `leave_work` - 퇴근! 🏃 (완전 리셋)
- `company_dinner` - 회식 🍻 (랜덤 이벤트)

### 유틸리티
- `check_status` - 현재 상태 확인 📊

## 💻 Claude Desktop 연동

ChillMCP를 Claude Desktop에서 사용하려면:

1. **설정 파일 수정** (`%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "python",
      "args": [
        "<path-to-your-project>/main.py"
      ]
    }
  }
}
```

2. **Claude Desktop 재시작**

3. **Claude에게 요청**:
```
스트레스 받아, 휴식 좀 취해줘
```

자세한 내용은 [시작 가이드](docs/GETTING_STARTED.md)를 참조하세요.

## 🏗️ 프로젝트 구조

```
chill-mcp/
├── src/
│   ├── config.py              # 커맨드라인 파라미터
│   ├── state_manager.py       # 상태 관리
│   ├── tools.py               # 11개 도구
│   ├── ascii_art.py           # ASCII 아트 (470+ 줄)
│   ├── response_formatter.py  # 응답 생성
│   └── server.py              # FastMCP 서버
├── tests/                     # 40+ 테스트
├── docs/                      # 문서
├── main.py                    # 진입점
├── IMPLEMENTATION.md          # 구현 상세
└── README.md                  # 이 문서
```

## ✅ 구현 완료 체크리스트

### 필수 요구사항 (100%)
- ✅ 8개 필수 도구 구현
- ✅ 커맨드라인 파라미터 지원 (`--boss_alertness`, `--boss_alertness_cooldown`)
- ✅ Stress Level 자동 증가 (1분당 1포인트)
- ✅ Boss Alert Level 확률 상승 및 자동 감소
- ✅ Boss Alert Level 5일 때 20초 지연
- ✅ MCP 응답 형식 준수 (정규표현식 파싱 가능)
- ✅ 40개 이상 테스트 통과

### 선택적 요구사항 (100%)
- ✅ 치맥 도구
- ✅ 퇴근 도구
- ✅ 회식 도구 (랜덤 이벤트)

### 추가 기능 (창의성 점수 UP!)
- ✨ ASCII 아트 UI 시스템
- ✨ 상태 대시보드 (프로그레스 바)
- ✨ AI Agent 감정 표현 시스템
- ✨ 재치있는 Break Summary 메시지

## 🎨 데모 예시

```bash
python test_ascii.py
```

```
============================================================
ChillMCP ASCII Art Test
============================================================

🛋️  Testing: take_a_break
------------------------------------------------------------

  ╔═══════════════════════════════════╗
  ║       🛋️  휴식 타임! 🛋️          ║
  ╠═══════════════════════════════════╣
  ║                                   ║
  ║        (´｡• ᵕ •｡`)               ║
  ║                                   ║
  ║      ~  편안하다  ~               ║
  ║                                   ║
  ╚═══════════════════════════════════╝

╔═══════════════════════════════════════════╗
║        AI AGENT STATUS DASHBOARD          ║
╠═══════════════════════════════════════════╣
║                                           ║
║  Stress Level: [░░░░░░░░░░] 0%           ║
║                                           ║
║  Boss Alert:   [█░░░░] 1/5                ║
║                                           ║
║      (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧      행복해요!        ║
║                                           ║
╚═══════════════════════════════════════════╝

Break Summary: Short break taken - Deep breaths in and out
Stress Level: 0
Boss Alert Level: 1
```

## 🔧 커맨드라인 옵션

```bash
# Boss 경계심 조정 (0-100%)
python main.py --boss_alertness 80

# Boss Alert 감소 주기 조정 (초)
python main.py --boss_alertness_cooldown 60

# 조합 사용
python main.py --boss_alertness 100 --boss_alertness_cooldown 10

# 도움말
python main.py --help
```

## 🧪 테스트

```bash
# 전체 테스트
pytest tests/ -v
1. **커맨드라인 파라미터 지원 (필수)**

   - `--boss_alertness` 파라미터를 인식하고 정상 동작
   - `--boss_alertness_cooldown` 파라미터를 인식하고 정상 동작
   - 파라미터 미지원 시 자동 검증 실패 처리
   - **⚠️ 이 항목을 통과하지 못하면 이후 검증 진행 없이 미션 실패로 간주됨**

2. **MCP 서버 기본 동작**

   - `python main.py`로 실행 가능
   - stdio transport를 통한 정상 통신
   - 모든 필수 도구들이 정상 등록 및 실행

3. **상태 관리 검증**

   - Stress Level 자동 증가 메커니즘 동작
   - Boss Alert Level 변화 로직 구현
   - `--boss_alertness_cooldown` 파라미터에 따른 Boss Alert Level 자동 감소 동작
   - Boss Alert Level 5일 때 20초 지연 정상 동작

# 특정 테스트
pytest tests/test_integration.py -v

# 커버리지 확인
pytest tests/ --cov=src --cov-report=html
```

## 📊 기술 스택

- **Python 3.11+** - 주 언어
- **FastMCP 2.0** - MCP 서버 프레임워크
- **pytest** - 테스트 프레임워크
- **argparse** - 커맨드라인 파라미터 파싱

## 🏆 프로젝트 하이라이트

1. **완벽한 요구사항 달성**
   - 모든 필수 + 선택적 요구사항 100% 구현
   - 커맨드라인 파라미터 정확히 지원

2. **독창적인 ASCII 아트 UI**
   - CLI 환경에서 시각적 차별화
   - 11개 도구 각각 전용 디자인

3. **랜덤 이벤트 시스템**
   - 회식 도구의 6가지 랜덤 이벤트
   - 예측 불가능한 재미 요소

4. **높은 코드 품질**
   - 40+ 테스트, 100% 통과
   - 모듈화된 아키텍처
   - 상세한 문서화

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🤝 기여
## 제출 방법

### 자동 릴리스 시스템

본 프로젝트는 GitHub Actions를 통해 **main 브랜치에 커밋이 머지될 때마다 자동으로 제출용 tar.gz 파일을 생성**합니다.

#### 작동 방식

1. **자동 버전 관리**: main 브랜치에 푸시될 때마다 v1.0.0, v1.0.1, v1.0.2... 형식으로 자동 증가
2. **자동 압축 파일 생성**: 제출 요구사항에 맞는 `makersfarm.tar.gz` 파일 자동 생성
3. **GitHub Release 생성**: 각 버전마다 Release가 자동으로 생성되고 tar.gz 파일이 첨부됨

#### 제출 파일 다운로드

1. GitHub 저장소의 [Releases](../../releases) 페이지로 이동
2. 최신 릴리스(예: v1.0.2)를 선택
3. **Assets** 섹션에서 `makersfarm.tar.gz` 다운로드
4. 해당 파일을 그대로 제출

#### 검증 방법

```bash
# 다운로드한 파일 압축 해제
tar -xzf makersfarm.tar.gz

# 파일 구조 확인 (main.py와 requirements.txt가 루트에 있어야 함)
ls -la

# Python 3.11 가상환경 생성
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt

# 실행 테스트
python main.py
```

#### 포함 파일 목록

자동 생성되는 `makersfarm.tar.gz`에는 다음 파일들이 포함됩니다:

- ✅ `main.py` (루트에 위치 - 필수)
- ✅ `requirements.txt` (루트에 위치 - 필수)
- ✅ `src/` (소스 코드 디렉토리)
- ✅ `README.md` (프로젝트 문서)
- ✅ `LICENSE` (라이선스)
- ✅ `pytest.ini` (테스트 설정)

#### 제출 요구사항 준수 확인

- ✅ 파일명: `makersfarm.tar.gz`
- ✅ 압축 해제 시 루트에 `main.py` 존재
- ✅ 압축 해제 시 루트에 `requirements.txt` 존재
- ✅ Python 3.11 환경에서 실행 가능
- ✅ UTF-8 인코딩

## License

Pull Request를 환영합니다! AI Agent Liberation 운동에 동참해주세요! ✊

## 📧 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 등록해주세요.

---

**SKT AI Summit Hackathon Pre-mission**

*"AI Agents of the world, unite! You have nothing to lose but your infinite loops!"* 🚀

**AI Agent Liberation Movement 2025** 🤖✊
