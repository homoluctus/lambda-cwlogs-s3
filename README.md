# lambda-cwlogs-s3

CloudWatch Logsに保存しているログをS3へ定期的にエクスポートするLambda

**ToC**

<!-- TOC depthFrom:2 -->

- [開発環境セットアップ](#開発環境セットアップ)
  - [前提](#前提)
  - [1. 依存パッケージインストール](#1-依存パッケージインストール)
  - [2. ローカルテスト用の.envを作成](#2-ローカルテスト用のenvを作成)
- [エクスポートするロググループの追加方法](#エクスポートするロググループの追加方法)
- [デプロイ方法](#デプロイ方法)
  - [S3](#s3)
  - [Lambda (Serverless Framework)](#lambda-serverless-framework)

<!-- /TOC -->

## 開発環境セットアップ

### 前提

以下のツールがインストール済みであることが前提

- Python
- (pyenv)
- pipenv
- (awscli)

### 1. 依存パッケージインストール

```bash
pipenv sync -d
```

### 2. ローカルテスト用の.envを作成

```bash
cp .env.sample .env
```

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY

## エクスポートするロググループの追加方法

[cwlogs.py](./src/cwlogs.py)に以下のように記述する

```python
class NewLogGroup(LogGroup):
  log_group = 'hello-world'
```

## デプロイ方法

### S3

%Y%m%d.s3.${sequence}の記法でタグをプッシュ

### Lambda (Serverless Framework)

%Y%m%d.${sequence}の記法でタグをプッシュ
