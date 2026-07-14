# GitHub Pages source diagnostic

## Before
```json
{
  "url": "https://api.github.com/repos/Damian545-DJ/raport-publiczny/pages",
  "status": "built",
  "cname": null,
  "custom_404": false,
  "html_url": "https://damian545-dj.github.io/raport-publiczny/",
  "build_type": "workflow",
  "source": {
    "branch": "main",
    "path": "/"
  },
  "public": true,
  "protected_domain_state": null,
  "pending_domain_unverified_at": null,
  "https_enforced": true
}
```

## Update result
```text
{
  "message": "Resource not accessible by integration",
  "documentation_url": "https://docs.github.com/rest/pages/pages#update-information-about-a-apiname-pages-site",
  "status": "403"
}

HTTP_STATUS:403
```

## After
```json
{
  "url": "https://api.github.com/repos/Damian545-DJ/raport-publiczny/pages",
  "status": "built",
  "cname": null,
  "custom_404": false,
  "html_url": "https://damian545-dj.github.io/raport-publiczny/",
  "build_type": "workflow",
  "source": {
    "branch": "main",
    "path": "/"
  },
  "public": true,
  "protected_domain_state": null,
  "pending_domain_unverified_at": null,
  "https_enforced": true
}
```
