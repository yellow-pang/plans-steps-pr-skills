# Commit message contract

```text
<type>(<optional-scope>): <검증된 결과를 설명하는 한글 제목>

변경:
- 실제 변경 목적과 주요 결과
- 리뷰에 필요한 계약 또는 흐름 변화

Verification:
- 실제 실행한 command와 결과
```

Allowed default types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `style`, `ci`, `build`.

Before using the message, list **Explicitly staged paths** and confirm each belongs to the one purpose. Omit the scope when it adds no clarity. Omit the body only for a genuinely self-explanatory change with no verification detail needed; never invent a Verification entry.
