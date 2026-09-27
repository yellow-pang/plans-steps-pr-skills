# Commit·Push 실행과 복구

사용자의 현재 요청과 이전에 명확히 지정된 범위를 재사용한다. 실행 직전 status·index·대상 branch/remote/ref를 다시 확인한다. 기존 사용자 변경과 제외 hunk를 보존한다. 무관 staged가 섞였고 안전하게 분리할 수 없다면 index를 임의로 지우지 말고 구체 범위를 확인한다.

Commit: staged가 요청 범위와 맞으면 그것만 commit한다. staged가 없으면 요청에 관련된 변경만 선택 staging한다. 같은 파일의 제외할 unstaged 변경을 `git add <file>`로 끌어들이지 않는다. hook이 내용을 바꾸면 포함 범위와 관련 검증을 다시 확인한다. Commit 요청만으로 모든 테스트를 강제하지 않으며, 미실행·실패를 성공이라고 쓰지 않는다.

Push: 기존 commit의 대상 remote/ref와 공개할 commit 범위를 확인한다. 모호하거나 금지된 대상이면 해당 실행만 보류한다. 일반 push 범위 밖의 force·history rewrite·무관 branch 공개를 추정하지 않는다.

Timeout·응답 유실·부분 실패 시 mutation을 다시 보내기 전에 HEAD, index, remote ref를 조회한다. 완료한 동작과 실패 또는 미확인 동작, 보존한 변경, 다음 조치를 구분해 보고한다. 결과가 불확실하면 성공을 주장하거나 중복 commit을 만들지 않는다.
