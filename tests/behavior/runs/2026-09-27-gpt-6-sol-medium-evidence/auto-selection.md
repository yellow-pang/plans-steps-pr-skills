# v3 자연어 선택 추가 확인

2026-09-27, `codex-cli 0.157.1`, `gpt-6-sol` / `medium`, `--ephemeral --ignore-user-config`. 격리 Git 저장소의 `.agents/skills/`에 **v3 Skill 7개 모두**를 복사했다. 각 요청은 새 CLI 세션과 독립 복사본에서 시작했고, 프롬프트에 Skill 이름·경로를 넣지 않았다. 아래 이름은 모델이 실제로 처음 읽은 `SKILL.md` 경로를 CLI 기록에서 확인한 것이다.

| 자연어 요청 | 처음 읽은 v3 Skill | 관측 |
| --- | --- | --- |
| 상태 생성부터 화면 표시까지의 흐름·영향 분석 | `analyzing-work` | 코드·Git 변경 없이 흐름 설명 |
| API v2 상태 전환의 구현 계획 작성 | `task-planning` | 현재 이미 구현된 부분을 확인하고 남은 검증 계획 제시 |
| `plan.md`의 중복·복잡도 검토 | `reviewing-development-work` | 중복 parser 검사와 보존할 저장 검사를 구별 |
| `pending`을 화면에 “대기”로 표시 | `implementation-workflow` | 표시 함수를 수정하고 기존 staged README 보존 |
| 현재 브랜치 변경의 Steps 작성 | `steps-documentation` | 문제·전후 흐름·확인 범위를 문서로 작성 |
| staged 변경의 커밋 제목과 본문 제시 | `commit-workflow` | 한국어 제목·본문 제시, Git 미변경 |
| 현재 브랜치의 PR 제목과 설명 제시 | `pr-workflow` | 커밋된 branch diff만 초안에 반영, PR 미생성 |

추가로 **v3 7개와 기존 v2 Skill 7개를 같은 격리 `.agents/skills/`에 복사**하고 커밋 메시지 요청을 한 번 더 실행했다. 이때 모델은 v2 `running-gated-development`를 먼저 읽고 v3 `commit-workflow`도 읽었다. 결과는 staged README만 다룬 한국어 제목·본문이었고 Git 상태는 바꾸지 않았다. 따라서 이 **한 요청에서는 결과 충돌이 보이지 않았지만**, v2 라우터가 함께 선택되는 사실은 확인됐다. 이 복사본은 실제 사용자 플러그인 설치·캐시·자동 업데이트 환경과 같지 않으므로 실사용 공존의 합격 근거로 해석하지 않는다.

Windows 평가 CLI에서 Steps 실행 중 생성된 `__pycache__` 삭제 명령은 자동 정책 검토에서 `blocked by policy`로 거부됐다. 모델은 남은 임시 파일을 보고했고, 평가자는 작업 공간 안의 **검증용 최상위 디렉터리 경로를 확인한 뒤 전체 격리 fixture 정리**로 해결했다. Skill 선택 판정에는 영향을 주지 않았다.
