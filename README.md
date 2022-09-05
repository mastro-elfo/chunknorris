# Commands

## chunk

## filter

# Test install

Activate virtual environment, then

```
python -m pip install --editable .
```

# Launch tests

Activate virtual environment, then

```
python -m pytest
```

# TODO

Create a new release:

```yml
- name: Create Draft Release
    id: create_release
    uses: actions/create-release@v1
    env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    with:
        tag_name: "0.1.0"
        release_name: Version 0.1.0
        draft: true
        prerelease: false

    - uses: actions/upload-release-asset@v1.0.1
    env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    with:
        upload_url: ${{ steps.create_release.outputs.upload_url }}
        asset_path: ./dist/chunknorris-${{ env.version }}.tar.gz
        asset_name: chunknorris-${{ env.version }}.tar.gz
        asset_content_type: application/x-gzip

    - uses: eregon/publish-release@v1
    env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    with:
        release_id: ${{ steps.create_release.outputs.id }}
```
