---
name: pr-workflow
description: PR 제목·본문을 준비하거나, 명시된 요청에 따라 PR을 생성·설명 갱신할 때 사용합니다. PR 설명 요청만으로 원격 변경을 실행하지 않습니다.
---

# PR Workflow

요청의 완료 지점을 구별한다. **PREPARE**는 제목·본문·리뷰 정보만 제공하며 staging·commit·push·PR 생성/갱신을 하지 않는다. **EXECUTE**는 명시된 PR 생성 또는 지정 PR의 제목·본문 갱신을 수행한다. PR 요청은 미커밋 변경의 자동 commit이나 merge·reviewer 지정을 포함하지 않는다.

적용 지침과 PR 관례, base/head, 커밋된 전체 branch diff를 확인한다. staged·unstaged·untracked는 PR에 아직 포함되지 않은 변경으로 따로 구분한다. 실제 변경, 계약·실행 흐름, 영향, 검증 기록과 제한을 바탕으로 리뷰어가 이해할 제목·본문을 작성한다. Plan/Steps가 없어도 진행하고 확인하지 못한 효과나 검증 성공을 쓰지 않는다. base나 범위가 불명확하면 확인 가능한 초안과 한계를 제공한다. 파일 작성을 요청받았다면 사용자 지정 위치 → 저장소 관례 → `docs/pr/`를 따르고, 설명만 요청됐다면 응답으로 제공한다.

EXECUTE에서는 [Provider 작업](references/provider-operations.md)을 읽는다. 확정된 committed head를 PR 생성에 필요한 경우에만 허용된 일반 push로 공개할 수 있다. 대상·공개 범위가 모호하거나 push가 금지됐다면 해당 실행을 보류하고 준비 자료를 제공한다. 지정 PR 설명 갱신은 요청된 필드만 수정한다. 성공은 실제 provider 조회의 PR 식별자·URL·head/base·상태로 확인한다.
