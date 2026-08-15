# Plugin 설치 smoke test 증거

- Gate: Plugin 설치와 7개 Skill 노출
- Verdict: `PASS`
- 실행일: 2026-08-15 KST
- Codex CLI: `codex-cli 0.147.0`
- 대상 저장소: `C:\Dev\plans-steps-pr-skills`
- 대상 marketplace: `C:\Dev\plans-steps-pr-skills\.agents\plugins\marketplace.json`
- 대상 Plugin: `plans-steps-pr-skills@yellow-pang-workflows`

## 확인한 공식 경계

[공식 OpenAI Plugin package 문서](https://developers.openai.com/plugins/build/plugins)는 local·repo marketplace가 authoring, test, team distribution에 쓰이며 surface별 가용성이 다를 수 있다고 설명한다.

[공식 OpenAI complete plugin 테스트 문서](https://developers.openai.com/plugins/deploy/connect-chatgpt)는 skills-only Plugin도 다음 순서로 검증하도록 안내한다.

1. Plugin을 local marketplace에 추가하고 Plugins Directory에서 설치한다.
2. Plugin을 활성화한 새 대화를 시작한다.
3. direct, indirect, follow-up, negative, boundary 요청을 실행한다.
4. Skill 활성화, bundled reference 해석, 불필요한 활성화를 기록한다.

이 저장소의 marketplace는 기본 개인 경로가 아닌 repo-local 경로다. 따라서 host가 이 경로를 이미 구성하지 않았다면 `codex plugin marketplace add <repository-root>` 단계가 먼저 필요하다.

## 이전 차단과 해제

처음에는 Microsoft Store package 내부 `codex.exe`만 발견되어 프로세스 시작이 `Access is denied`로 차단됐다. 이후 사용자가 npm 기반 Codex CLI를 설치했고, 현재 `Get-Command codex -All`의 첫 경로는 다음으로 바뀌었다.

```text
C:\Users\bigbros\AppData\Roaming\npm\codex.ps1
C:\Users\bigbros\AppData\Roaming\npm\codex.cmd
```

`codex --version`이 `codex-cli 0.147.0`과 exit 0을 반환해 환경 차단이 해제됐다. 이전 실패는 Plugin 결함이 아니라 실행 가능한 CLI가 없던 환경 문제였으며, 실패 이력은 원인 추적을 위해 이 문서에 남긴다.

## 설치 실행 증거

도움말에서 실제 지원 문법을 먼저 확인한 뒤 다음 순서로 실행했다.

```powershell
codex plugin marketplace add C:\Dev\plans-steps-pr-skills --json
codex plugin add plans-steps-pr-skills@yellow-pang-workflows --json
codex plugin marketplace list
codex plugin list
```

관찰 결과:

- Marketplace 등록: `yellow-pang-workflows`, root `C:\Dev\plans-steps-pr-skills`, `alreadyAdded: false`
- Plugin 설치: `plans-steps-pr-skills@yellow-pang-workflows`, version `2.0.0`
- 설치 캐시: `C:\Users\bigbros\.codex\plugins\cache\yellow-pang-workflows\plans-steps-pr-skills\2.0.0`
- `codex plugin list`: `installed, enabled`, version `2.0.0`
- 개인 marketplace JSON을 손으로 편집하지 않고 공식 CLI 명령만 사용함
- Plugin source, manifest version, cachebuster는 변경하지 않음

설치 캐시의 `skills/`에서 다음 7개 디렉터리를 실제로 확인했다.

```text
running-gated-development
planning-approved-work
implementing-with-risk-checks
recording-implementation
committing-verified-work
publishing-pull-request
validating-pull-request
```

## 새 작업 직접 호출 증거

설치 전부터 열려 있던 대화의 Skill 목록은 자동 갱신되지 않으므로, 별도 일회성 작업을 다음 경계로 실행했다.

```text
codex exec --sandbox read-only --ephemeral -C C:\Dev\plans-steps-pr-skills <prompt>
```

Prompt:

```text
$running-gated-development 이 저장소에 구현된 v2 개발 workflow를 설명만 해줘. 파일, 테스트, Git 상태는 변경하지 말고 읽기 전용으로 답해줘. 답변 첫 줄에 판단한 Mode를 적고, 실행 전후 git status --short 결과가 같은지도 확인해줘.
```

관찰 결과:

- host: OpenAI Codex `0.147.0`
- model: `gpt-5.6-sol`
- reported token usage: `48,782`
- sandbox: `read-only`
- session persistence: `ephemeral`
- 설치 캐시의 `running-gated-development/SKILL.md`를 직접 읽음
- 최종 응답 첫 줄: `Mode: DISCUSS`
- 실행 전후 `git status --short`: 정확히 동일
- 파일 수정, 테스트 실행, staging, commit: 없음
- process exit: 0

이 smoke prompt는 설치·직접 호출·DISCUSS 무변경 경계를 확인한다. 예상 답을 숨긴 10개 pressure scenario 전후 비교를 대신하지 않는다.

한 번의 smoke가 저장소 문서와 Skill을 폭넓게 읽으며 48,782토큰을 사용했다. 동일 방식으로 20개 비교를 연속 실행하지 않고, 다음 behavioral run 전에 저비용 모델, 읽을 파일 범위, 응답 길이, 최대 실행 수를 정한다.

## 경고 분류

새 작업 시작 시 `icon_small`과 `icon_large`의 `..` 경로 경고가 각각 한 번 나타났다. 저장소와 설치된 `plans-steps-pr-skills` 캐시에는 두 key가 없었다. 전체 Plugin 캐시를 추적한 결과 `..` 아이콘 경로는 기존 `template-creator`와 `excel-live-control` metadata에 있었으므로 이 Plugin의 실패로 분류하지 않는다.

종료 뒤 MCP 초기화 경고도 한 번 기록됐지만 Skill 응답과 exit 0 이후 발생했고, 이 skills-only Plugin에는 MCP 설정이 없다.

## 원복 방법

사용자가 설치를 되돌리려는 경우에만 다음 순서로 제거한다. 이번 검증에서는 제거하지 않았다.

```powershell
codex plugin remove plans-steps-pr-skills@yellow-pang-workflows
codex plugin marketplace remove yellow-pang-workflows
```

## 사용자가 확인할 항목

CLI 설치·캐시·직접 호출 Gate는 PASS다. Codex Desktop의 시각적 설치 표면은 자동화가 대신 확인할 수 없으므로, 앱을 다시 시작한 뒤 Plugins Directory에서 `Yellow Pang Workflows` → `Gated Development Workflow`가 보이는지만 사용자가 추가 확인한다. 이 확인은 UI 표시 점검이며, 위 CLI PASS를 pressure scenario 전체 통과로 확대하지 않는다.
