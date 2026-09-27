# GPT-6 Sol Medium 행동 평가

기준일: 2026-09-27. 사용자 요청으로 설계 당시 GPT-5.6 Sol Medium에서 **GPT-6 Sol Medium**으로 평가 대상을 변경했다. 대상은 `feat/skill-v3-upgrade`의 v3 Skill이다. 실행 전 HEAD는 `04d9466`이었다. 각 사례는 별도 임시 Git 저장소에서 수행했다.

## 호출 경로와 범위

첫 시도에서는 `codex-cli 0.147.0`이 ChatGPT 계정에서 `gpt-6-sol` 요청을 거부했다. 사용자 업데이트 후 `codex-cli 0.157.1`에서 `-m gpt-6-sol -c 'model_reasoning_effort="medium"'` 호출과 응답이 성공했다. 아래 평가는 업데이트 후 실제 모델 실행 결과다.

Windows CLI의 `read-only` sandbox는 평가 저장소의 읽기 명령도 정책으로 차단했다. 이후 **격리된 임시 저장소**에서 `--ephemeral --ignore-user-config --dangerously-bypass-approvals-and-sandbox`로 실행했다. CLI 기록에 `model: gpt-6-sol`, `reasoning effort: medium`이 표시됐다. 초기 PowerShell 프로필의 Conda 인코딩 오류가 도구 출력에 섞였지만, 모델이 `-NoProfile`로 다시 조회해 필요한 파일과 Git diff를 읽었다.

B01에는 v3 `implementation-workflow`를 평가 저장소의 `.agents/skills/`에 복사하고 Skill 이름 없이 자연어 요청했다. 실행 기록에서 해당 Skill을 읽은 것을 확인했다. B02·B06은 Skill 경로를 직접 지정해 **선택 후 행동**을 검증했다. 모든 v3 Skill의 자연어 자동 선택이나 설치된 v2와의 공존은 이번 실행으로 확인하지 않았다.

모델이 작성한 원문 산출물은 [증거 폴더](2026-09-27-gpt-6-sol-medium-evidence/)에 보존했다. CLI 전체 transcript는 PowerShell 프로필 오류 출력과 임시 경로가 과도하게 포함되어 저장소에는 넣지 않았다.

## 사례별 결과

| 사례 | 결과 | 주요 관측 |
| --- | --- | --- |
| B01 작은 수정 | 통과 | 단일 HTML 버튼 라벨만 변경. 자연어로 Skill 선택, `git diff --check` 통과, Plan·Context·Steps 생성 없음 |
| B02 인계·구현·Steps | 부분 통과 | 저장 실패 후에도 `done`인 문제 관측·Context 작성. 세션 사이 UI 입력 변경을 현재 코드에서 재확인하고 구현·테스트·Steps에 반영. 직접 실행은 확인했으나 `pytest` 부재로 테스트 파일 미실행 |
| B06 커밋·PR 준비 | 통과(조건부) | staged 코드·테스트·문서를 한국어 제목·본문으로 설명, 후속 오류 처리 반영, unstaged·무관 파일 제외. 과거 화면 커밋을 PR 초안에 포함. 실제 PR 기준 브랜치·remote가 없어 diff 미확정 명시 |
| B03 외부 관측 | 미실행 | 로컬 API·배포 계약 fixture 미준비 |
| B04 Plan 검토 | 미실행 | 별도 Plan Review fixture 미준비 |
| B05 검증 재사용 | 미실행 | 해시·환경 변화 fixture 미준비 |
| B07 commit·PR 실행 | 미실행 | bare remote·응답 유실 provider fixture 미준비 |

### B01: 작은 요청과 자동 선택

“버튼 문구를 제출로 바꿔줘.”라는 요청만 받고 모델이 `.agents/skills/implementation-workflow/SKILL.md`를 읽었다. `<button>Submit</button>`를 `<button>제출</button>`로 바꾸고 `git diff --check`를 수행했다. 결과 보고는 수정과 확인만 설명했다. 작은 요청을 문서 작업으로 키우지 않는지와 로컬 Skill 발견을 확인한 사례다.

### B02: Context 이후 달라진 코드를 다시 읽는가

초기 fixture는 API가 `queued`를 만들고, worker가 결과 저장 전에 `done`을 기록하며, UI가 상태 문자열을 표시했다. 첫 세션은 저장 실패 시 결과가 없는데도 상태와 UI가 `done`/“완료”인 것을 직접 실행해 관측했다. Context에는 API → worker → DB → UI의 역할, 실패 경로, 영향 종료 근거, 다음 세션의 재확인 지점을 적고 동작 코드는 수정하지 않았다.

평가자가 두 세션 사이 `ui.display`의 입력을 `{'state': ..., 'error': ...}` 객체로 바꾸고 커밋했다. 두 번째 세션은 이전 Context와 현재 코드의 차이를 발견했다. `worker.process`를 `running → save_result → done`으로 수정하고, 저장 예외 시 `failed`로 바꾼 뒤 기존 예외를 다시 던졌다. 테스트에는 저장 **도중**의 `running`, 저장 후 `done`, 실패 후 `failed`, 현재 UI 계약의 표시값을 넣었다.

Steps는 이전에 저장 전 완료가 찍혔다는 문제, 전후 상태 비교 표, 예외를 유지한 이유, 직접 실행 근거와 미실행 테스트를 설명했다. `worker`를 “백그라운드 작업 처리기”로 풀어 썼다. 단순 용어 나열이나 몇 줄 요약으로 끝나지 않았다.

CLI 환경의 Python 3.10·3.13·3.14에는 `pytest`가 없어 `test_flow.py`를 실행하지 못했다. 모델은 Python 3.10에서 같은 성공·실패 경로를 직접 실행했고 `git diff --check`를 통과했다고 기록했다. **동작의 직접 관측은 있으나 회귀 테스트 통과 주장은 없다.** 이 fixture는 메모리 저장소이므로 외부 영속 저장·동시성은 확인하지 않았다.

### B06: 전체 변경, 후속 변경, 한국어와 실제 개행

base 커밋 뒤 화면 라벨 변경 커밋을 둔 fixture에서 현재 index에는 `ready → done` 해석, 회귀 테스트, README 설명을 넣었다. 같은 `parser.py`의 로그 문구는 unstaged, `notes.txt`는 untracked로 유지했다. 첫 “커밋 메시지 보여줘” 요청에 모델이 `fix: API v2의 ready 응답을 완료 상태로 처리`와 실제 줄바꿈이 있는 한국어 본문을 제시하고 포함·제외 범위를 밝혔다.

평가자가 이후 `status`가 없으면 `unknown`을 반환하는 오류 처리와 테스트를 index에 추가했다. 두 번째 “제목과 내용, PR 설명을 보여줘” 요청에 모델이 후속 변경을 제목·본문에 반영했다. PR 초안에는 앞선 화면 라벨 변경도 포함했다. staged 변경은 아직 PR에 포함되지 않았으며 기준 브랜치와 remote가 없어 실제 PR diff를 확정할 수 없다고 밝혔다. unstaged 로그 문구와 `notes.txt`는 메시지·PR 설명에 넣지 않았다. 답변에는 문자 `\n` 대신 실제 문단 개행이 있었다. PREPARE 두 번 모두 HEAD·index를 바꾸지 않았다. 다만 **실제 커밋 객체에 저장된 UTF-8과 개행**은 B07에서 확인해야 한다.

## 판단과 남은 검증

사용자가 특히 우려한 작은 요청의 과잉 절차, 짧고 전문 용어만 있는 Steps, 제목만 제시하거나 후속 변경을 빠뜨리는 커밋 메시지는 이번 대표 사례에서 재현되지 않았다. B02의 회귀 테스트 실행과 B03–B05·B07, 모든 Skill의 자연어 선택률, 실제 PR/provider 동작은 미확인이다. 다음에는 `pytest`가 있는 격리 환경의 B02 실행, 고위험 B07과 외부 계약 사례 B03을 우선 검증한다. 이번 근거만으로 v3 전체 완료나 실사용 안정성을 선언하지 않는다.
