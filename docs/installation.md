# v3 설치·교체와 사용 안내

v3는 개발 작업을 맡는 독립 Skill 7개다. 이 저장소의 `main`에서 받아 사용하며 플러그인 설치는 필요하지 않다. 처음에는 실제로 작업할 프로젝트 하나에 적용해 문서 품질과 요청 처리를 확인한 뒤 사용 범위를 넓힐 수 있다.

## 설치할 파일과 위치

설치 대상은 `skills/` 바로 아래의 **7개 Skill 폴더 전체**다. 각 폴더의 `SKILL.md`와 `references/`를 함께 복사한다. 루트 `README.md`, `docs/`, `tests/`는 설명·설계·평가 자료로, Skill 실행을 위한 설치 대상은 아니다.

| 사용 범위 | 설치 위치 |
|---|---|
| 먼저 적용할 프로젝트 하나 | `<프로젝트>/.agents/skills/<Skill 이름>/` |
| 사용자 계정의 모든 프로젝트 | `<사용자 홈>/.agents/skills/<Skill 이름>/` |

Codex는 프로젝트와 사용자 범위의 `.agents/skills`에서 Skill을 찾으며, 같은 이름의 복사본을 자동으로 하나로 합치지 않는다. 설치 위치와 명시 호출 방법의 기준은 [OpenAI의 Skills 안내](https://learn.chatgpt.com/docs/build-skills)다. 아래 절차는 이 저장소의 이전 버전에서 v3로 교체하는 경우를 다룬다.

## 이전 main의 Skill 교체

1. 현재 세션의 Skill 목록에서 실제로 읽는 `SKILL.md` 경로를 확인한다. 프로젝트·사용자 범위의 `.agents/skills/`와 이전에 직접 설치한 위치를 확인한다. 과거에 `.codex/skills/`를 사용했다면 그 경로도 확인한다. 경로가 존재한다는 이유만으로 현재 로딩된다고 단정하지 않는다.
2. **이 저장소에서 가져온 아래 5개**의 기존 복사본과 사용자 수정 내용을 백업한다. 백업은 프로젝트 밖 별도 폴더 등 Skill 검색 경로 밖에 둔다. 같은 `skills/` 안에서 이름만 `-old`로 바꾸면 옛 Skill이 계속 발견될 수 있다.
3. 기존 5개를 실제 설치 위치에서 제거하거나 백업 위치로 옮긴 뒤 새 7개를 설치한다. 다른 저장소의 Skill, 사용자 전용 Skill, 시스템 Skill은 유지한다. 여러 범위에 중복 설치했다면 이전 복사본이 함께 노출되지 않도록 정리한다.
4. v2 플러그인도 설치한 환경이면 플러그인 관리 화면에서 별도로 비활성화하거나 제거한다. 캐시 파일을 직접 고치는 방법으로 교체하지 않는다. v2 Git 브랜치를 지울 필요는 없다.

| 이전 main에 설치했던 이름 | v3에서의 처리 |
|---|---|
| `task-planning` | 같은 이름의 새 폴더로 교체 |
| `implementation-workflow` | 같은 이름의 새 폴더로 교체 |
| `steps-documentation` | 같은 이름의 새 폴더로 교체 |
| `preparing-commit` | 기존 폴더 제거 후 `commit-workflow` 설치 |
| `pr-documentation` | 기존 폴더 제거 후 `pr-workflow` 설치 |
| 없음 | `analyzing-work`, `reviewing-development-work` 추가 |

기존 프로젝트의 `AGENTS.md`나 별도 설정에 옛 Skill 이름·경로가 적혀 있다면 해당 참조도 갱신한다. 예전 Plan·Steps·Context는 개발 근거이므로 Skill 교체를 이유로 삭제하지 않는다. 프로젝트 지침이 과거 절차를 강제하는 경우에는 새 Skill 설치만으로 그 규칙까지 바뀌지 않으므로 의도에 맞는지 따로 확인한다.

## main에서 받아 설치하기

아래 PowerShell 예시는 **새로 내려받는 원본 폴더**와 **이미 존재하는 적용할 프로젝트**를 사용한다. 경로 두 개를 자신의 환경에 맞게 바꾼다. 기존 Skill의 백업·정리는 위 절차로 먼저 진행한다. 같은 이름의 대상 폴더가 있으면 덮어쓰지 않고 중단한다.

```powershell
$skillSource = 'C:\Dev\plans-steps-pr-skills-source'
$targetProject = 'C:\Dev\my-project'

if (Test-Path -LiteralPath $skillSource) {
    throw '원본 경로가 이미 있습니다. 새 경로를 지정하거나 기존 저장소의 main을 확인하세요.'
}
if (-not (Test-Path -LiteralPath $targetProject -PathType Container)) {
    throw '적용할 프로젝트 경로를 확인하세요.'
}
git clone --branch main --single-branch https://github.com/yellow-pang/plans-steps-pr-skills.git $skillSource
if ($LASTEXITCODE -ne 0) { throw '저장소를 내려받지 못했습니다.' }

$skillNames = @(
    'analyzing-work', 'task-planning', 'reviewing-development-work',
    'implementation-workflow', 'steps-documentation',
    'commit-workflow', 'pr-workflow'
)
$installRoot = Join-Path $targetProject '.agents\skills'
foreach ($skillName in $skillNames) {
    $sourceFolder = Join-Path (Join-Path $skillSource 'skills') $skillName
    $targetFolder = Join-Path $installRoot $skillName
    if (-not (Test-Path -LiteralPath (Join-Path $sourceFolder 'SKILL.md') -PathType Leaf)) {
        throw "원본 Skill이 없습니다: $skillName"
    }
    if (Test-Path -LiteralPath $targetFolder) {
        throw "기존 설치를 먼저 확인하세요: $targetFolder"
    }
}
New-Item -ItemType Directory -Path $installRoot -Force | Out-Null
foreach ($skillName in $skillNames) {
    $sourceFolder = Join-Path (Join-Path $skillSource 'skills') $skillName
    Copy-Item -LiteralPath $sourceFolder -Destination $installRoot -Recurse -ErrorAction Stop
}
git -C $skillSource rev-parse HEAD
```

마지막에 출력한 커밋 식별자(SHA)를 설치 출처로 기록한다. 복사 도중 오류가 났다면 생성된 대상 폴더를 확인하고 해당 설치분만 정리한 뒤 재시도한다. 사용자 범위 설치를 원하면 같은 7개 폴더를 사용자 홈의 `.agents/skills/`에 복사한다. 양쪽에 같은 Skill을 중복 설치할 필요는 없다.

이미 이 저장소를 내려받았다면 새 clone 대신 작업 트리와 브랜치를 확인한 뒤 병합된 `main`을 원본으로 사용해도 된다. 사용자 수정이 있는 저장소에 강제 초기화나 덮어쓰기를 하지 않는다. 프로젝트에 설치한 Skill을 팀과 공유할지는 그 프로젝트의 저장소 관리 방침에 따라 결정한다.

## 설치 후 확인

적용할 프로젝트에서 새 Codex 세션을 열고 목록과 경로를 확인한다. CLI·IDE에서는 `/skills` 또는 `$`로 Skill을 명시할 수 있고, 앱에서는 제공되는 Skill 선택 메뉴를 사용한다. 표시되지 않으면 세션을 다시 시작한다. 구체적인 UI는 [공식 안내](https://learn.chatgpt.com/docs/build-skills)를 따른다.

- 새 7개 이름이 의도한 설치 경로에서 발견되는가?
- 이전 `preparing-commit`, `pr-documentation`이나 중복된 옛 복사본이 함께 노출되지 않는가?
- `references/`를 포함한 설치 파일이 내려받은 원본과 같은가?
- 자연어 요청에서 적절한 Skill을 읽는가? 선택이 안 되면 먼저 이름을 명시해 발견 문제와 행동 문제를 구분한다.

main 병합, 로컬 원본 갱신, 프로젝트에 복사한 Skill 교체는 서로 다른 단계다. main을 갱신한 뒤에도 설치된 복사본은 별도로 교체해야 한다. 새 설치 경로를 읽는 것이 확인되기 전에는 새 버전의 동작을 평가했다고 기록하지 않는다.

## 요청별 사용 예시

각 Skill은 필요한 때 따로 사용한다. 분석 → 계획 → 검토 → 구현 → Steps → 커밋 → PR 전체를 매번 거칠 필요는 없다.

| 원하는 일 | 요청 예시 | 기대하는 완료 지점 |
|---|---|---|
| 원인·영향 분석 | “저장 실패인데 완료로 표시되는 원인과 영향 범위를 분석해줘.” | 현재 코드·관측 근거와 미확인 사항 설명 |
| 긴 작업 인계 | “다음 세션에서 이어갈 수 있도록 현재 판단과 남은 작업을 Context로 남겨줘.” | 인계 문서 작성; 재개 시 현재 코드 재확인 |
| 구현 계획 | “중복 상태 처리를 줄이는 구현 계획만 작성해줘.” | 변경 위치·선택 이유·완료 조건·검증 계획 |
| 계획·구현 검토 | “이 계획에서 불필요한 구조와 꼭 유지할 검사·경계를 검토해줘.” | 제거·유지 의견과 근거; 자동 코드 수정 없음 |
| 작은 수정 | “이 버튼 문구를 제출로 바꿔줘.” | 필요한 수정과 그에 맞는 확인 |
| 여러 단계 구현 | “합의한 계획대로 구현하고 관련 테스트까지 진행해줘.” | 요청 범위 구현·검증 결과; 해결된 선택 재승인 없음 |
| Steps 문서 | “이번 작업 전체의 변경 이유와 전후 흐름·검증을 한국어 Steps 문서로 작성해줘.” | 실제 완료 내용, 쉬운 용어 설명, 필요한 예시·표·흐름도, 제한 기록 |
| 커밋 준비 | “현재 변경의 커밋 메시지 제목과 본문을 보여줘.” | 대상 diff 전체를 설명하는 한국어 제목·본문; Git 상태 유지 |
| 커밋 실행 | “이 변경을 커밋해줘.” | 요청된 변경의 커밋과 저장된 메시지 확인 |
| Push 실행 | “현재 커밋을 origin의 이 브랜치에 push해줘.” | 대상 원격 브랜치 반영 확인 |
| PR 준비 | “main과 비교해서 PR 제목과 본문을 보여줘.” | 브랜치 전체 변경과 검증·제한 설명; 미커밋 변경 구분 |
| PR 생성 | “이 브랜치로 main 대상 PR을 생성해줘.” | 필요한 일반 push, 기존 PR 조회, 생성 결과 확인 |

메시지·설명 요청은 실행 요청과 다르다. 커밋 요청만으로 push·PR을 실행하지 않고, PR 생성 요청만으로 미커밋 변경을 커밋하거나 main에 병합하지 않는다. 한 번에 여러 결과를 원하면 “변경을 커밋하고 PR을 만들어 main에 병합해줘”처럼 완료 지점을 함께 지정한다. 병합은 명시된 사용자 요청과 저장소 권한·보호 규칙에 따라 처리한다.

## 실제 프로젝트에서 평가할 것

GPT-6 Sol Medium의 [대표 행동 평가](../tests/behavior/runs/2026-09-27-gpt-6-sol-medium.md)는 이미 기록되어 있다. B02 테스트는 당시 관측한 결과로 재구성했고 B03·B07은 로컬 서비스와 가짜 PR 도구를 사용했다. 실제 설치 환경, 다른 Skill·플러그인, GitHub/Gitea 연동에서의 동작까지 입증한 결과는 아니다.

처음에는 평소 개발 요청을 그대로 사용하며 다음을 확인한다.

- 작은 수정에 불필요한 Plan·Steps·승인 절차를 추가하지 않는가?
- 분석 결과와 현재 코드를 다시 대조하고 데이터가 만들어져 저장·표시되는 영향 범위를 확인하는가?
- Steps가 용어 목록으로 끝나지 않고 문제·이유·전후 동작을 이해할 수 있게 설명하는가? 전문 용어에 짧은 설명을 붙이고 표·흐름도를 필요한 때 사용하는가?
- 커밋 메시지가 한국어 제목·본문으로 현재 대상의 주요 변경을 빠짐없이 설명하는가? 실제 저장된 메시지에 문자 `\n` 대신 줄바꿈이 있는가?
- 실행 요청의 범위를 지키고, 성공·실패·미실행을 실제 근거와 맞게 보고하는가?

문제가 생기면 사용 모델·추론 수준, 설치한 SHA와 읽은 Skill 경로, 원래 요청, 기대한 결과와 실제 결과, 관련 diff·실행 근거를 함께 남긴다. 인증정보나 프로젝트 비밀은 제외한다. 선택 자체가 잘못됐는지, 선택된 Skill의 설명이 부족했는지, 다른 프로젝트 지침과 충돌했는지 구분하면 수정할 위치를 찾기 쉽다.

Steps 품질 개선은 `skills/steps-documentation/SKILL.md`의 핵심 규칙과 `references/writing-guide.md`의 상세 기준·예시를 함께 살펴본다. 문서가 짧다는 이유만으로 규칙을 늘리기보다 이해하기 어려웠던 실제 산출물과 누락된 설명을 기준으로 보완한다.

## 다음 업데이트와 되돌리기

업데이트할 때는 현재 설치본과 사용자 수정을 백업하고 새 main의 변경을 확인한 뒤 7개 폴더를 교체한다. 설치본에서 직접 고친 내용은 원본과 비교해 필요한 수정만 반영한다. 옛 폴더 위에 무조건 복사하면 삭제된 파일이 남을 수 있으므로 확인된 기존 설치분을 먼저 분리한다.

되돌릴 때는 이번에 설치한 v3 7개만 설치 위치에서 분리하고 백업한 이전 설치본을 원래 위치로 복원한다. 최초 main에서 v3로 교체하기 전에는 5개이고, 이후 v3 업데이트를 되돌릴 때는 이전의 7개다. 업데이트 때 바꾼 프로젝트 지침의 이름·경로 참조도 함께 복원한다. 새 세션에서 실제 로딩 경로를 확인한다. 프로젝트 코드·Plan·Steps·Context와 관련 없는 Skill은 그대로 유지한다.
