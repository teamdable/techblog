---
layout: post
title: "간단한 macOS 개발 환경 공유"
date: 2021-03-30 9:00:00 +0900
author: Dong-jin Ahn
tags: [안동진, dev, configuration]
---

안녕하세요? AP팀 안동진입니다. 팀 발표에서 가볍게 공유한 제 macOS 개발 환경을 소개합니다.

## Git 설정

사무실에는 회사에서 지급받은 노트북을 쓰지만, 재택근무를 할 때는 개인 노트북을 사용하고 있습니다. 이런 상황에서 업무 Git repo에 개인 이메일로 커밋 메세지를 남기고 싶지 않고, 회사용 Github 계정이 별도로 설정되어 개인 계정과는 다른 ssh key를 사용하기 때문에 저는 아래와 같은 설정을 사용합니다. 개인용 Git 디렉토리를 `~/git`, 업무용 Git 디렉토리를 `~/work`라 했을 때, 다음과 같이 설정합니다.

```
# ~/.gitconfig
[gpg]
    program = gpg
[commit]
    gpgSign = false
[tag]
    forceSignAnnotated = false
[includeIf "gitdir:~/work/"]
    path = .gitconfig-work
[includeIf "gitdir:~/git/"]
    path = .gitconfig-personal

[core]
    excludesfile = /Users/adoji/.gitignore
```

```
# ~/.gitconfig-work
[user]
    name = Dong-jin Ahn
    email = dongjin@dable.io
```

```
# ~/.gitconfig-personal
[user]
    name = Dong-jin Ahn
    email = adoji92@gmail.com
```

위와 같은 설정으로 `~/git`의 하위 디렉토리에서는 개인용 설정을, `~/work`의 하위 디렉토리에서는 업무용 설정을 사용할 수 있습니다.

---

개인용 ssh key를 `id_rsa`, `id_rsa.pub`, 업무용 ssh key를 `work_id_rsa`, `work_id_rsa.pub`라고 했을 때, Git repo의 Clone은 서비스에 따라 조금 다르게 클론해야합니다.

- github: `git clone git@github.com-dongjinahn:teamdable/hello.git`
- gitlab: `git clone git@{gitlab_id}.gitlab.com:teamdable/world.git`

---

Git repo를 private npm library로 사용하는 경우, npm install (또는 yarn) 이 사용하는 ssh key를 명시해줘야 정상적으로 진행할 수 있습니다.

`ssh-agent bash -c 'ssh-add /Users/adoji/.ssh/work_id_rsa; npm install'`


---

## tmuxinator

tmux(terminal multiplexer의 약자)를 더 잘 쓸 수 있게 도와주는 툴입니다. 관련 링크: https://blog.outsider.ne.kr/1167

```yaml
# ~/.tmuxinator/hello.yml
name: hello
root: /Users/adoji/dable/hello

windows:
- hello:
    layout: even-horizontal
    panes:
        - npm run start
- hello-git:
    layout: even-horizontal
    panes:
        - lg
- hello-sh:
    layout: even-horizontal
    panes:
        - echo hello!
```

위와 같은 설정으로 `tmuxinator start hello`를 실행하면 다음과 같은 tmux 창을 바로 사용할 수 있습니다. 여러 Git repo를 개발하고, 각 repo에서 사용하는 명령어가 많을 수록 유용합니다.

---

## .zshrc 심볼릭 링크

여러 대의 컴퓨터를 사용하는 경우 `.zshrc` 또는 `.bashrc`를 동기화하는 것을 선호합니다.

`ln -s ~/Google\ Drive/path/to/.zshrc ~/.zshrc`

위와 같이 구글 드라이브, 드롭박스와 같은 파일 동기화 프로그램과 사용하시면 좋습니다.

---

## 터미널 설정

### iTerm Hotkey 윈도우

![iterm 설정 스크린샷1](/techblog/assets/images/Simple-macOS-Dev-Env/iterm1.png)

iterm 설정 > keys > hotkey > create a dedicated hotkey window를 눌러 `ctrl + command + t`를 단축키로 hotkey window를 토글합니다.

![iterm 설정 스크린샷2](/techblog/assets/images/Simple-macOS-Dev-Env/iterm2.png)

그 뒤에는 profiles > hotkey window > window에서 transparency 0, rows 35로 사용합니다.

### iTerm Color profile & Oh my zsh

- 개인적으로 다음 컬러 프로파일을 선호합니다. https://gist.github.com/alicanb/a016334546ff501bdab73e623281fbd6
- Oh-my-zsh 테마로는 powerlevel10k. https://github.com/romkatv/powerlevel10k
- 폰트로는 Source code pro for powerline을 사용합니다. https://github.com/powerline/fonts
- Oh-my-zsh 플러그인으로는 다음을 사용합니다.
    1. zsh-autosugesstions: https://github.com/zsh-users/zsh-autosuggestions
        - ![iterm 사용 스크린샷1](https://camo.githubusercontent.com/16e72effec8df52a27e3aa9b1d24f37f86215d500d06ef18247d4206863a4f52/68747470733a2f2f61736369696e656d612e6f72672f612f33373339302e706e67)
        - 이전에 사용한 명령어들을 전부 다 입력하지 않아도 옅은 회색으로 보여줍니다.
    2. alias-tips: https://github.com/djui/alias-tips
        - ![iterm 사용 스크린샷2](/techblog/assets/images/Simple-macOS-Dev-Env/alias_tips.png)
        - 더 나은 alias가 있는 경우 표시합니다.
    3. fzf: https://github.com/junegunn/fzf
        - 터미널에서 fuzzy search를 도와주는 툴입니다.
        - ctrl + t로 fzf를 활성화하여 하위 디렉토리에 위치한 원하는 파일을 손쉽게 입력할 수 있습니다.

### 기타 추천

- [Loom](https://www.loom.com/): 화면을 쉽게 녹화하여 버그를 아카이빙하거나 이슈를 공유할 때 매우 유용합니다.
- [Sip](https://setapp.com/apps/sip): 모니터에 보이는 색의 색상 코드를 쉽게 복사할 수 있습니다.
    - true-tone display가 꺼져있어야 정상적으로 작동합니다.
- [Alfred font-awesome workflow](https://github.com/ruedap/alfred-font-awesome-workflow): alfred에서 빠르게 fa를 찾을 수 있도록 도와줍니다.
    - ![알프레드 폰트 어썸 워크플로우 동작 캡쳐](https://raw.githubusercontent.com/ruedap/alfred-font-awesome-workflow/assets/images/screencast-illustrator.gif)