---
layout: post
title: "엄청나게 빠른 자바스크립트 번들러, esbuild"
date: 2021-07-15 00:00:00 +0900
author: Yujin Min
tags: [ esbuild, webpack, bundler, 번들러, 웹팩 ]
---

![esbuild's rising stars](/techblog/assets/images/about-esbuild/esbuild-2020.png)
[2020년 가장 많은 별을 추가한 빌드툴 목록](https://risingstars.js.org/2020/en#section-build)

2020년에 첫 등장해 빠른 속도로 성장해가고 있는 esbuild를 소개해보려고 합니다.

![esbuild's speed](/techblog/assets/images/about-esbuild/esbuild-bundle-speed.png)

기존 번들러보다 100배 빠르다는 문구로 홍보하고 있는 esbuild는 현재 번들러 중 가장 유명하다고 할 수 있는 웹팩을 사용하며 불편함을 느낀 사람들에게 대안으로 떠오르고 있습니다. 번들러란 무엇인지, 웹팩의 단점, 그리고 esbuild가 다른 번들러에 비해 이토록 빠를 수 있는 이유에 대해 알아보겠습니다.

## 자바스크립트 번들러가 뭔가요?

자바스크립트 번들러는 하나의 JS 파일에 작성한 모든 코드와 그와 연관된 의존성들을 다 넣을 수 있게 도와주는 도구입니다. 팀에서 가장 많이 사용하고 있는 유명한 번들러로는 browserify와 웹팩이 있습니다. 왜 이런 번들러가 필요한 걸까요?

- 브라우저가 모듈 시스템을 전반적으로 지원하지 않아서
- 의존성을 비롯한 이미지, css 파일 등을 원하는 순서대로 적용할 수 있게 도와줘서

이외에도 파일 간 변수명 충돌과 같은 문제를 해결해 줄 수 있습니다. 만약 여러 js 파일을 브라우저에서 실행하게 된다면 순서 문제, 의존성 문제, 명확성 문제 등이 생길 수 있겠죠. 이런 문제를 해결하기 위해 자바스크립트 모듈 시스템이 나왔고 번들러는 모듈을 하나로 합쳐 브라우저에서 사용할 수 있게 도와줍니다.

## 웹팩의 단점

![webpack npm](/techblog/assets/images/about-esbuild/webpack.png)

[webpack](https://www.npmjs.com/package/webpack)은 현재 시점에서도 가장 많이 다운로드되고 사용되는 번들러입니다. 관련된 플러그인, 생태계만 해도 그 수가 상당할 정도로 사랑을 받고 있습니다. 하지만 웹팩을 사용해보신 분이라면 시간이 갈수록 아래와 같은 문제를 마주하셨을 거라 생각합니다.

- 개발 시 재빌드가 생각보다 느리다
- 설정이 어렵다

웹팩에서 플러그인, 로더를 추가할수록, 앱이 복잡하고 커져갈수록 수정한 부분을 다시 확인할 때까지 점점 더 느려지는 현상을 겪어보신 적이 있을 겁니다. 스택오버플로우에서도 really slow, too slow와 같은 단어와 함께 설정을 어떻게 바꾸면 될지, 어떤 부분이 문제인지에 대한 질문을 다수 찾아볼 수 있고 빌드 속도를 빠르게 할 수 있는 방법을 알려주는 글들도 인터넷에 굉장히 많습니다. 빌드 속도가 느려지면서 개발 효율성이 악화되고 빌드를 다시 최적화하지만 프로젝트가 커져가면서 다시 빌드 속도가 느려지는 것입니다. 그래서 번들러들 중에는 개발 모드에서는 번들링을 사용하지 않는 경우도 종종 있습니다.

컴파일 타임만큼이나 많은 주니어 개발자들을 힘들게 하는건 웹팩의 설정입니다. HMR(브라우저를 새로 고침하지 않아도 확인 가능하게 해준다)은 어떻게 적용해야 하는 것인지, 로더와 플러그인은 어디에 어떤 순서로 넣어야 하는 것인지 등등 단순히 설정(configure)만 하는 것도 공부가 많이 필요한 것으로 악명이 높습니다.

## esbuild

![esbuild npm](/techblog/assets/images/about-esbuild/esbuild.png)

[esbuild](https://www.npmjs.com/package/esbuild)는 상대적으로 최근에 나온 번들러로 모든 기능, 모든 환경을 지원하지는 않습니다. 그럼에도 불구하고 번들링 속도 만으로도 한 번쯤은 건드려보고 싶게 만드는 esbuild에 대해 알아보겠습니다. 

아래는 esbuild가 왜 빠른가에 대한 FAQ의 일부입니다. 자세한 답변이 궁금하시다면 [공식 링크](https://esbuild.github.io/faq)에서 찾아보실 수 있습니다.

1) 대부분의 번들러는 자바스크립트로 작성되어 있습니다. 고로 작성된 esbuild가 자바스크립트를 파싱하는 동안 노드는 번들러의 자바스크립트를 파싱해야하고 노드가 번들러의 자바스크립트를 파싱을 끝내는 순간 이미 esbuild는 모든 걸 끝낸 뒤일 것입니다. 아직 번들러가 번들링을 시작도 안한 시점에!

2) 고는 자바스크립트와 달리 병렬 구조가 핵심인 언어입니다. 가능한 한 모든 CPU core를 사용하게 되어있습니다. 보통 파싱, 링킹, 코드 생성의 3단계를 거쳐야 하는데 가장 많은 일을 해야 하는 파싱과 코드 생성이 전부 병렬적으로 작동하게 되어있습니다. 모든 쓰레드가 메모리를 공유하고 있어서 다른 엔트리 포인트를 지니고 있는 자바스크립트 라이브러리들을 번들링 하는 일을 쉽게 공유할 수 있습니다. 요즘 대부분의 컴퓨터는 많은 코어를 가지고 있으니까요!

3) 써드 파티 라이브러리를 사용하는 대신에 모든 게 처음부터 작성된 상태입니다. 많은 작업이 필요하지만 퍼포먼스를 처음부터 고려할 수 있고 일관성 있는 데이터 구조를 사용하며 필요할 때 설계의 변화도 줄 수 있습니다.

4) 메모리를 효율적으로 사용합니다. 컴파일러는 이상적으로 O(n)의 복잡도를 가지고 있는데 적게 넣을수록 빠르겠죠. esbuild는 그 횟수를 3번으로 최소화하고 [AST](https://itnext.io/ast-for-javascript-developers-3e79aeb08343)(프로그래밍 언어의 문법에 따라 소스 코드 구조를 표시하는 계층적 프로그램 표현) 데이터의 재활용을 최대화하는 반면에 다른 번들러들은 하나의 단계도 여러번으로 나눠서 처리합니다. 예를 들어 esbuild는 binding symbols, minifying syntax, JSX/TS to JS, and ESNext-to-ES2015를 하나로 처리하는 반면에

- string→TS→JS→string
- string→JS→older JS→string
- string→JS→minified JS→string

와 같이 처리하면 메모리도 더 많이 쓰고 더 느려질 것입니다.

## esbuild-loader

esbuild의 장점을 알겠는데 이미 웹팩의 설정을 끝마치고 오랜 기간 사용하고 있다면 [esbuild-loader](https://www.npmjs.com/package/esbuild-loader)를 써보는 것은 어떨까요? bable-loader, ts-loader 등을 대체해 더 빠른 빌드를 기대할 수 있습니다.

적용 방법도 간단합니다. babel-loader를 사용하고 있는 경우 웹팩 설정에서 아래와 같이 바꿔주면 바로 적용됩니다. 한 번 시도해 보세요!

```js
  module.exports = {
    module: {
      rules: [
-       {
-         test: /\.js$/,
-         use: 'babel-loader',
-       },
+       {
+         test: /\.js$/,
+         loader: 'esbuild-loader',
+         options: {
+           loader: 'jsx',  // Remove this if you're not using JSX
+           target: 'es2015'  // Syntax to compile to (see options below for possible values)
+         }
+       },

        ...
      ],
    },
  }
```