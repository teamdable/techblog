---
layout: post
title:  "Biome: 차세대 JS Linter와 Formatter"
date:   2024-05-16 10:00:00 +0900
author: Heeyoung Jang
tags: [ Biome, Linter, Formatter ]
---

안녕하세요. 데이블 Service Front-end Team(SF Team)의 장희영입니다.

이 글에서는 JavaScript에서 Code Formatter와 Linter 역할을 동시에 수행하는 Biome이라는 도구를 소개해보려고 합니다.

## 들어가기 전에…

혹시 Prettier라는 Code Formatter를 들어본 적이 있으신가요? 아마 프론트엔드 개발자라면 모를 수가 없을 것으로 생각합니다.

Prettier는 지배적인 위치를 차지하고 있는 Code Formatter입니다. 그러나 Prettier는 이러한 독보적인 입지 탓에 경쟁이 부족하여 성능 개선이나 다양한 엣지 케이스 해결에 대한 동기가 부족하다고 생각했습니다.

그래서 Prettier팀은 선의의 경쟁을 유도하기 위해 상금을 걸고 “Rust로 프로젝트를 만들어서, Prettier 테스트 스위트의 95%를 통과해라”라는 [대회를 개최](https://console.algora.io/challenges/prettier)하게 되었습니다. 

![prettier bounty](/assets/images/biome-js-linter-and-formatter/prettier-bounty.png)

Biome을 소개하는 글이라고 했는데, 왜 갑자기 이런 얘기를 하느냐고요?

바로 Biome이 이 대회에서 우승을 차지한 프로젝트이기 때문입니다.

Biome은 그렇게 등장했습니다. 하지만 어디서 갑자기 혜성처럼 나타난 것은 아니었습니다.

그 배경에는 2020년에 등장한 Rome이라는 프로젝트가 있습니다. 이 프로젝트는 JavaScript 툴 체인으로서 번들링, 컴파일, 포매팅, 린팅, 테스트 등의 모든 작업을 하나의 CLI에서 수행할 수 있는 올인원 솔루션을 지향했습니다. 하지만 회사가 어려워지고 모든 직원이 해고되면서 결국 Rome은 중단되고 말았습니다.

그럼에도 불구하고 Rome에 대한 애정이 남아있던 일부 인원들이 이를 포크하여 새로운 프로젝트를 만들었는데, 이 프로젝트가 바로 Biome입니다.

상표권 문제로 인해 Rome이라는 이름은 그대로 사용하지 못했고, “Bis(다시) + Rome“의 의미를 담아 “Biome”이라는 이름을 붙였다고 합니다.

## 그럼 이제, 본격적으로 Biome을 살펴보도록 하겠습니다.

![biome docs](/assets/images/biome-js-linter-and-formatter/biome-docs.png)

Biome은 공식 사이트에서 "웹 프로젝트를 위한 툴체인"이라고 설명하고 있습니다.

2023년 9월 작성된 공식 블로그 포스팅에 의하면, Biome은 360° 툴체인이 되고자 하며, 이를 위해 컴파일러의 기초 작업을 시작했다고 합니다.

하지만 현재로서는 Code Formatter와 Linter의 기능만 제공하고 있습니다.

Biome은 Prettier와 97% 호환되는 매우 빠른 Code Formatter와 JavaScript 및 TypeScript를 위한 고성능 Linter를 한 번에 사용할 수 있다고 하는데요,

## 한 번 직접 사용해봅시다.

(npm을 기준으로 진행합니다)

먼저 Biome을 설치합니다.

```bash
npm install --save-dev --save-exact @biomejs/biome
```

그다음 아래 명령어를 통해 설정 파일을 초기화합니다.

```bash
npx @biomejs/biome init
```

그러면 `biome.json`이라는 이름으로 아래와 같은 내용이 담긴 설정 파일이 생성됩니다. 이때 `--jsonc` 옵션을 사용한다면 `.jsonc` 확장자의 설정 파일을 생성할 수 있습니다.

```json
{
	"$schema": "https://biomejs.dev/schemas/1.7.3/schema.json",
	"organizeImports": {
		"enabled": true
	},
	"linter": {
		"enabled": true,
		"rules": {
			"recommended": true
		}
	}
}
 
```

이 설정 파일에 원하는 설정을 추가해주면 됩니다. [설정에 관한 설명](https://biomejs.dev/reference/configuration/)과 [Linter의 Rule에 관한 설명](https://biomejs.dev/linter/rules/)은 공식문서에서 확인할 수 있습니다.

만약 ESLint와 Prettier를 사용하고 있었다면 해당 설정을 그대로 마이그레이션 해서 사용할 수도 있습니다.

```bash
npx @biomejs/biome migrate eslint --write
npx @biomejs/biome migrate prettier --write
```

이렇게 하면 프로젝트에 존재하는 ESLint와 Prettier의 설정 파일을 읽고, 해당 설정을 Biome으로 가져올 수 있습니다.

설정을 마쳤다면 직접 사용해볼 차례입니다.

#### 1. format

```bash
npx biome format --write <files>
```

`format` 명령어와 `--write` 옵션을 사용하면 포맷이 적용된 파일을 새로 쓸 수 있습니다. 즉 Code Formatter의 역할을 합니다.

#### 2. lint

```bash
npx biome lint --apply <files>
```

`lint` 명령어와 `—apply` 옵션을 사용하면  Linter로 사용할 수 있습니다. `--apply` 옵션의 경우, 코드의 의미를 변경하지 않는 선에서 코드를 안전하게 변경해줍니다. 

만약 코드의 의미를 변경해야 하는 부분이라면, 변경하지 않고 에러를 발생시켜 해당 부분을 알려주게 됩니다.

![biome error](/assets/images/biome-js-linter-and-formatter/biome-error.png)

이런 부분들까지 변경해도 괜찮다고 한다면, `--apply-unsafe` 옵션을 사용하라고 합니다.

#### 3. check

```bash
npx biome check --apply <files>
```

`format` 과 `lint` 명령을 모두 수행하는 것이 `check` 명령입니다. Linter와 Code Formatter의 역할을 동시에 수행할 수 있는 Biome의 장점을 적극적으로 활용할 수 있는 명령어입니다.

간단하게 사용법을 소개해드렸는데요, 사실 코드를 작성할 때마다 매번 해당 명령을 입력하는 것은 다소 비효율적인 일입니다. 그래서 보통은 git hook에 등록하여 커밋 전에 해당 명령이 수행될 수 있도록 설정하거나, 에디터와 통합하여 파일을 저장할 때마다 포맷을 지정해주는 format on save 기능을 활용하여 Biome을 사용하기를 권장합니다.

[공식 문서](https://biomejs.dev/guides/integrate-in-editor/)를 확인하면 에디터별로 어떻게 Biome을 통합하여 사용할 수 있는지 확인할 수 있습니다. 저는 VSCode를 사용하고 있어서 Biome VSCode 확장을 사용하고 있는데요, VSCode 기준으로 확장은 잘 적용되고 있습니다.


![biome extention suggestion](/assets/images/biome-js-linter-and-formatter/biome-suggestion.png)

제안도 잘 보여주고요,

![biome extention format on save](/assets/images/biome-js-linter-and-formatter/biome-format-on-save.gif)

format on save 기능도 잘 동작합니다!

## 그래서 사용해보니까요…

몇 가지 장단점이 눈에 띄었습니다.

#### 장점 1. 설정이 간단합니다

만약 TypeScript 환경에서 ESLint와 Prettier를 사용한다고 하면 

- ESLint 설정
    - eslint 설치
    - typescript-eslint/parser 설치
    - typescript-eslint/eslint-plugin 설치
    - 설정 파일 작성
- Prettier 설정
    - prettier 설치
    - 설정 파일 작성
- Prettier와 ESLint를 동시에 사용하기 위한 설정
    - eslint-config-prettier 설치
    - eslint-plugin-prettier 설치
    - 설정 파일 수정

이러한 과정들을 거쳐야 합니다. 여러 가지 방법이 있을 수도 있겠지만, 보통은 그렇습니다. 설치한 패키지만 해도 5개가 됩니다. 하지만 Biome을 사용한다면,

- Biome 설정
    - biome 설치
    - 설정 파일 작성

이렇게 간단하게 설정을 마칠 수 있습니다.

#### 장점 2. 속도가 빠릅니다

공식문서에 따르면 Biome은 Prettier보다 25배 빠르다고 합니다. 하지만 제가 경험한 환경에서는 이 부분에 대한 체감이 크지 않아,`time` 명령어를 사용하여 직접 실행 시간을 비교해보았습니다.

최근에 저희 팀이 Biome을 도입한 프로젝트가 있는데요, 해당 프로젝트에서 Biome 도입 전 Prettier 명령어의 수행 시간과 Biome 명령의 실행 시간을 아래 명령어를 통해 측정해보았습니다.

```bash
time npx biome format --write src/**/*.js src/**/*.ts ## biome
time npx prettier --write src/**/*.js src/**/*.ts ## prettier
```

![prettier time](/assets/images/biome-js-linter-and-formatter/prettier-time.png)

Prettier는 명령어가 실행되는데 실제로 경과한 시간(real 항목)이 1.53초였고,

![biome time](/assets/images/biome-js-linter-and-formatter/biome-time.png)

Biome은 0.45초가 소요되었습니다.

이 프로젝트는 JS와 TS를 동시에 사용하고 있었으며, MacBook Pro (M3, 2023) 환경에서 약 150개 파일을 대상으로 수행 시간을 측정한 결과인데, 이 정도 규모에서는 Biome이 약 세 배 정도 빠른 것을 확인할 수 있었습니다. 

25배라는 수치는 더욱 정교한 환경에서의 테스트를 통해 도출된 결과일 것으로 생각합니다. 제가 경험한 환경에서는 그 정도의 차이는 아니었지만, Biome이 Prettier보다 빠르다는 점은 알 수 있었습니다.

#### 단점 1. CSS, HTML, Vue 등 아직 지원하지 않는 언어가 꽤 있습니다

아래는 현재 Biome의 지원 범위를 나타내는 표입니다.

- ✅: Supported
- 🚫: Not in progress
- ⌛️: In progress
- ⚠️: Partially supported (with some caveats)

![biome support language](/assets/images/biome-js-linter-and-formatter/biome-support.png)

저는 주로 React를 사용하여 개발하므로 고민 없이 Biome을 도입해볼 수 있었습니다. 그러나 부분적으로 지원되는 Vue나 Svelt를 사용할 때에는 Biome을 도입하기 어려울 수 있습니다.

여담이지만 저는 개인 블로그를 Gatsby라는 프레임워크를 사용하여 운영하고 있는데요, GraphQL과 Markdown을 주로 사용하고 있으므로 이 경우에도 Biome을 도입할 수 없겠습니다.

#### 단점 2. 레퍼런스가 부족합니다

아직 레퍼런스가 부족한 것이 단점으로 느껴졌습니다. 이는 제가 Biome에 대해 포스팅을 작성한 이유 중 하나이기도 합니다.

그러나 공식 문서가 잘 정리되어 있어 사용에 큰 어려움은 없었고, 사용자가 늘어나면 자연스럽게 해결될 문제로 보입니다.

## 결론

Biome은 린팅과 포매팅을 위한 통합 솔루션을 제공하여, ESLint와 Prettier와 같은 별도의 도구를 사용하는 것보다 더 빠르고 편리한 환경을 제공합니다. Biome의 빠른 속도와 간편한 설정은 개발자 경험과 생산성을 모두 향상시킬 수 있어, 최신 웹 개발 프로젝트에 유용한 자산이 될 수 있습니다.

현재로서는 ESLint와 Prettier를 Biome으로 대체하는 프로젝트가 그리 많지는 않지만, 간편한 설정과 빠른 속도만으로도 충분한 가치가 있는 프로젝트라고 생각합니다. 따라서 Biome이 중단된 프로젝트의 후계자라는 꼬리표에서 벗어나, 더 나은 성능과 개발자 경험을 제공하여 안정적인 툴체인으로 새롭게 자리매김하고 발전해 나갈 것을 기대합니다.