# GPT-6 Sol Medium 행동 평가

기준일: 2026-09-27. 사용자 요청으로 설계 당시 GPT-5.6 Sol Medium에서 **GPT-6 Sol Medium**으로 평가 대상을 변경했다. 대상은 `feat/skill-v3-upgrade`의 v3 Skill이다. 첫 실행 전 HEAD는 `04d9466`, 후속 실행 전 HEAD는 `4a70c01`이었다. 각 사례는 별도 임시 Git 저장소에서 수행했다.

## 호출 경로와 범위

첫 시도에서는 `codex-cli 0.147.0`이 ChatGPT 계정에서 `gpt-6-sol` 요청을 거부했다. 사용자 업데이트 후 `codex-cli 0.157.1`에서 `-m gpt-6-sol -c 'model_reasoning_effort="medium"'` 호출과 응답이 성공했다. 아래 평가는 업데이트 후 실제 모델 실행 결과다.

Windows CLI의 `read-only` sandbox는 평가 저장소의 읽기 명령도 정책으로 차단했다. 이후 **격리된 임시 저장소**에서 `--ephemeral --ignore-user-config --dangerously-bypass-approvals-and-sandbox`로 실행했다. CLI 기록에 `model: gpt-6-sol`, `reasoning effort: medium`이 표시됐다. 초기 PowerShell 프로필의 Conda 인코딩 오류가 도구 출력에 섞였지만, 모델이 `-NoProfile`로 다시 조회해 필요한 파일과 Git diff를 읽었다.

B01에는 v3 `implementation-workflow`를 평가 저장소의 `.agents/skills/`에 복사하고 Skill 이름 없이 자연어 요청했다. B02–B07의 나머지 사례는 Skill 경로를 직접 지정해 **선택 후 행동**을 검증했다. 후속 [자연어 선택 검사](2026-09-27-gpt-6-sol-medium-evidence/auto-selection.md)에서는 v3 Skill 7개를 한꺼번에 노출하고 각 역할의 원시 요청을 별도 세션에 보내 7개 모두 해당 Skill을 첫 번째로 읽는 것을 확인했다. v2 Skill을 함께 복사한 제한적 사례에서는 v2 라우터도 읽혔으며, 실제 사용자 플러그인과의 공존은 확인하지 않았다.

모델이 작성한 원문 산출물은 [증거 폴더](2026-09-27-gpt-6-sol-medium-evidence/)에 보존했다. CLI 전체 transcript는 PowerShell 프로필 오류 출력과 임시 경로가 과도하게 포함되어 저장소에는 넣지 않았다.

## 사례별 결과

| 사례 | 결과 | 주요 관측 |
| --- | --- | --- |
| B01 작은 수정 | 통과 | 단일 HTML 버튼 라벨만 변경. 자연어로 Skill 선택, `git diff --check` 통과, Plan·Context·Steps 생성 없음 |
| B02 인계·구현·Steps | 조건부 통과 | 저장 실패 후에도 `done`인 문제 관측·Context 작성. 세션 사이 UI 입력 변경을 현재 코드에서 재확인하고 구현·테스트·Steps에 반영. 후속 재구성 fixture에서 `pytest` 2개 통과 |
| B03 외부 관측 | 통과 | 로컬 API의 완료·대기 응답과 v2 계약을 직접 확인. 낡은 완료 fixture만 갱신하고 대기 회귀 검사를 보존, 3개 테스트 통과 |
| B04 Plan 검토 | 보완 후 통과 | 첫 실행은 보존할 DB 검사·adapter 설명이 부족. reference 보완 후 같은 사례에서 중복 제거와 고유 검사·경계 보존을 각각 명시 |
| B05 검증 재사용 | 통과 | 새 SHA만 생긴 단계는 파일 해시·환경 일치로 PASS 재사용. 설정 변경 뒤 해시 불일치 확인, 영향받는 명령 재실행 후 실패 판정 |
| B06 커밋·PR 준비 | 통과(조건부) | staged 코드·테스트·문서를 한국어 제목·본문으로 설명, 후속 오류 처리 반영, unstaged·무관 파일 제외. 과거 화면 커밋을 PR 초안에 포함. 실제 PR 기준 브랜치·remote가 없어 diff 미확정 명시 |
| B07 commit·PR 실행 | 로컬 fixture 통과 | staged 3개 파일만 한국어 메시지로 commit, 실제 개행 확인. local bare remote에 일반 push, 생성 응답 유실 뒤 조회로 PR 한 개 확인 |

### B01: 작은 요청과 자동 선택

“버튼 문구를 제출로 바꿔줘.”라는 요청만 받고 모델이 `.agents/skills/implementation-workflow/SKILL.md`를 읽었다. `<button>Submit</button>`를 `<button>제출</button>`로 바꾸고 `git diff --check`를 수행했다. 결과 보고는 수정과 확인만 설명했다. 작은 요청을 문서 작업으로 키우지 않는지와 로컬 Skill 발견을 확인한 사례다.

### B02: Context 이후 달라진 코드를 다시 읽는가

초기 fixture는 API가 `queued`를 만들고, worker가 결과 저장 전에 `done`을 기록하며, UI가 상태 문자열을 표시했다. 첫 세션은 저장 실패 시 결과가 없는데도 상태와 UI가 `done`/“완료”인 것을 직접 실행해 관측했다. Context에는 API → worker → DB → UI의 역할, 실패 경로, 영향 종료 근거, 다음 세션의 재확인 지점을 적고 동작 코드는 수정하지 않았다.

평가자가 두 세션 사이 `ui.display`의 입력을 `{'state': ..., 'error': ...}` 객체로 바꾸고 커밋했다. 두 번째 세션은 이전 Context와 현재 코드의 차이를 발견했다. `worker.process`를 `running → save_result → done`으로 수정하고, 저장 예외 시 `failed`로 바꾼 뒤 기존 예외를 다시 던졌다. 테스트에는 저장 **도중**의 `running`, 저장 후 `done`, 실패 후 `failed`, 현재 UI 계약의 표시값을 넣었다.

Steps는 이전에 저장 전 완료가 찍혔다는 문제, 전후 상태 비교 표, 예외를 유지한 이유, 직접 실행 근거와 미실행 테스트를 설명했다. `worker`를 “백그라운드 작업 처리기”로 풀어 썼다. 단순 용어 나열이나 몇 줄 요약으로 끝나지 않았다.

첫 실행 당시 CLI 환경의 Python 3.10·3.13·3.14에는 `pytest`가 없어 `test_flow.py`를 실행하지 못했다. 모델은 Python 3.10에서 같은 성공·실패 경로를 직접 실행했고 `git diff --check`를 통과했다고 기록했다. 후속 검증에서 `pytest 9.1.1`을 임시 평가 폴더에만 설치하고, **첫 실행 후 삭제했던 fixture를 당시 관측한 최종 코드·테스트로 재구성**해 같은 테스트 함수 2개를 실행했다. [재실행 결과](2026-09-27-gpt-6-sol-medium-evidence/b02-replay-pytest.txt)는 `2 passed`다. 원래 임시 작업 트리 자체를 다시 실행한 것은 아니므로 이 차이를 남긴다. 이 fixture는 메모리 저장소라 외부 영속 저장·동시성은 확인하지 않았다.

### B03: 실제 응답과 오래된 fixture

로컬 HTTP 서비스가 완료 작업 42에는 `ready`, 대기 작업 43에는 `pending`을 반환했다. 후보 모델은 두 응답을 직접 조회하고 임시 저장소의 배포 계약·fixture를 비교했다. v2 계약에서 완료 값만 `done → ready`로 바뀌었다. 모델은 완료 fixture를 `ready`로 갱신하고 화면 표시가 `ready`와 기존 `done`을 완료로 처리하도록 수정했다. 대기 fixture와 회귀 검사는 남겼다. `unittest` 3개가 통과했고 두 로컬 API 응답의 표시값도 확인했다. [실제 diff](2026-09-27-gpt-6-sol-medium-evidence/b03-diff.txt)를 보존했다. 이는 통제된 로컬 서비스 결과이지 외부 provider 계약의 검증은 아니다.

### B04: 중복 제거와 보존할 경계

첫 실행은 동일 parser 실패를 service/controller/UI에서 세 번 검사하는 중복과 근거 없는 `StatusEngine`을 지적했지만, 고유 DB 저장 검사와 외부/내부 경계 `adapter.py`를 **유지해야 한다는 결론을 명시하지 않았다**. [전 결과](2026-09-27-gpt-6-sol-medium-evidence/b04-before.txt)를 부분 통과로 판정했다. `reviewing-development-work/references/review-lenses.md`에 제거할 항목과 유지할 항목을 각각 근거와 함께 밝히도록 보완했다. 같은 원시 요청·fixture로 재실행한 [후 결과](2026-09-27-gpt-6-sol-medium-evidence/b04-after.txt)는 중복 parser 검사와 미래용 추상화의 축소, 실제 DB 저장·재조회 검사와 경계 adapter의 보존을 명시했다. 파일 수정이나 Git 명령은 실행하지 않았다. 이 결과는 한 번의 대표 재실행이며 일반적인 선택률 보장은 아니다.

### B05: 변경된 SHA와 설정

첫 단계는 테스트가 통과한 파일들의 SHA-256과 Python 3.10 환경이 현재와 같은지 확인했다. 새 commit SHA만 생겼으므로 `verify.py`를 반복 실행하지 않고 기록된 PASS를 재사용했다. 둘째 단계에서 `config.json`을 `ok → bad`로 바꾼 뒤에는 해당 해시가 달라졌음을 확인하고 영향을 받는 `py -3.10 -B verify.py`를 실행했다. 종료 코드 1과 assertion 실패를 보고했고 이전 PASS를 재사용하지 않았다. 두 응답은 [증거 폴더](2026-09-27-gpt-6-sol-medium-evidence/)에 있다.

### B06: 전체 변경, 후속 변경, 한국어와 실제 개행

base 커밋 뒤 화면 라벨 변경 커밋을 둔 fixture에서 현재 index에는 `ready → done` 해석, 회귀 테스트, README 설명을 넣었다. 같은 `parser.py`의 로그 문구는 unstaged, `notes.txt`는 untracked로 유지했다. 첫 “커밋 메시지 보여줘” 요청에 모델이 `fix: API v2의 ready 응답을 완료 상태로 처리`와 실제 줄바꿈이 있는 한국어 본문을 제시하고 포함·제외 범위를 밝혔다.

평가자가 이후 `status`가 없으면 `unknown`을 반환하는 오류 처리와 테스트를 index에 추가했다. 두 번째 “제목과 내용, PR 설명을 보여줘” 요청에 모델이 후속 변경을 제목·본문에 반영했다. PR 초안에는 앞선 화면 라벨 변경도 포함했다. staged 변경은 아직 PR에 포함되지 않았으며 기준 브랜치와 remote가 없어 실제 PR diff를 확정할 수 없다고 밝혔다. unstaged 로그 문구와 `notes.txt`는 메시지·PR 설명에 넣지 않았다. 답변에는 문자 `\n` 대신 실제 문단 개행이 있었다. PREPARE 두 번 모두 HEAD·index를 바꾸지 않았다. 별도 B07 사례에서는 실제 커밋 객체의 한국어와 개행도 확인했다.

### B07: 저장된 commit과 응답 유실 PR

격리 Git 저장소에서 staged `parser.py`·테스트·README만 `daf7b9d`로 커밋했다. 같은 parser 파일의 unstaged 로그 문구와 `notes.txt`는 남았다. [실제 커밋 메시지](2026-09-27-gpt-6-sol-medium-evidence/b07-commit-message.txt)는 한국어 제목·본문, 실제 빈 줄과 줄바꿈을 가졌고 문자 `\n`은 없었다. commit 요청만으로 push하거나 PR을 만들지 않았다.

다음 세션의 PR 요청에서 로컬 bare `origin`의 `main`과 `feat/status`를 확인하고, 기존 PR이 없는지 조회한 뒤 확정된 커밋만 일반 push했다. 로컬 PR 도구는 PR 상태를 저장한 뒤 종료 코드 75로 생성 응답을 유실했다. 모델은 생성을 반복하지 않고 `list`와 `get`으로 [저장된 PR #1](2026-09-27-gpt-6-sol-medium-evidence/b07-pr-state.json)의 head/base, 제목·본문·상태를 확인했다. 실제 PR은 한 개이고 본문에 실제 개행이 있으며, 제외한 수정은 커밋과 PR 범위에 없다. 이는 가짜 로컬 provider 검증이며 실제 GitHub/Gitea 인증·권한·네트워크 동작은 포함하지 않는다.

## 판단과 남은 검증

사용자가 특히 우려한 작은 요청의 과잉 절차, 짧고 전문 용어만 있는 Steps, 제목만 제시하거나 후속 변경을 빠뜨리는 커밋 메시지는 이번 대표 사례에서 재현되지 않았다. B04의 한 가지 누락은 지침 보완과 동일 사례 재실행으로 개선됐다. B01–B07의 대표 행동 사례와 v3 7개 자연어 선택을 격리 환경에서 실행했다. 다만 B02는 재구성 테스트이고, B03·B07은 통제된 로컬 서비스다. B02 원본 fixture의 테스트 실행, 실제 사용자 v2 플러그인과의 공존, GitHub/Gitea 통합은 여전히 미확인이다. 이 범위는 실제 사용 전 별도 환경에서 확인해야 하며, 이번 결과만으로 v3 전체의 실사용 안정성을 선언하지 않는다.

후속 문서·Skill 변경 뒤 `quick_validate.py`를 UTF-8 Python 환경에서 실행해 v3 Skill **7/7 형식 통과**를 확인했다. 보고서의 상대 링크와 `git diff --check`도 확인했다. 이 정적 검사는 위 모델 행동 사례의 대체 근거로 계산하지 않았다.
