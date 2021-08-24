---
layout: post
title: '드디어 Internet Explorer가 은퇴를 합니다'
date: 2021-08-24 00:00:00 +0900
author: Minji Cho
tags: [조민지, InternetExplorer, IE, Edge, IEmode]
---

안녕하세요, 데이블 Publisher Platform 위젯 개발 담당 조민지입니다.

지난 5월 19일, Internet Explorer(이하 IE) 데스크톱 앱에 대한 지원을 22년 6월 15일부로 종료할 것이라는 [Microsoft의 공식 발표](https://blogs.windows.com/windowsexperience/2021/05/19/the-future-of-internet-explorer-on-windows-10-is-in-microsoft-edge/)가 있었습니다.

<hr>

## 정말 D-300 인가

IE의 모든 플랫폼에 대한 지원이 22년 6월에 일괄 종료되는 것은 아닙니다.
하지만 종료 대상에 개인용 Windows 10의 IE 앱이 포함되고, 6월 공개된d Windows 11에서는 IE의 실행 자체가 막힌 것으로 보아 얼마 남지 않은 것은 확실해 보입니다.

22년 6월 이후에는 대부분 기업 대상의 지원이 유지됩니다. 아직 ActiveX를 사용하는 등 IE에 최적화된 사이트를 운영하는 기업을 위해, Microsoft는 Edge 브라우저에서 IE 모드라는 형태로 IE View를 지원하고 있습니다. 이 IE 모드마저도 지원이 종료되는 시점은 2029년입니다.

<br>

## Internet Explorer는 왜 공공의 적이 되었을까

IE가 90년대 말 브라우저 시장을 장악했던 데에는 분명 그만한 가치와 이유가 있었을 것입니다.

하지만 IE6 출시 이후 IE 팀이 Windows 팀에 통합되면서 버그 수정과 업데이트가 지연되고, 다른 브라우저들이 웹 표준을 구축해 가는 동안 IE는 그 자리에 머물러 있었습니다. 느린 속도에 [ActiveX](https://ko.wikipedia.org/wiki/%EC%95%A1%ED%8B%B0%EB%B8%8CX)의 보안 문제까지 더해지며 2009년에는 `No more IE6`라는 IE6 퇴출 캠페인이 일어나기도 했습니다.

모든 사용자의 모든 환경에서 동일하게 동작할 수 있어야 한다는 웹 표준을 무시한 IE를 우리가 무시하지 못하는 이유는, 여전히 IE를 사용하는 사용자가 있기 때문입니다.

21년 6월 기준, 전 세계적으로는 Chrome이 68.76%, Safari가 9.7%로 데스크톱 브라우저 시장의 대부분을 점유하고 있고, IE는 1.45%에 불과합니다. ([출처](https://gs.statcounter.com/browser-market-share/desktop/worldwide/#monthly-202106-202106-bar))
국내에서도 2016년부터는 Chrome이 IE를 앞질렀고, 이후 IE 사용률이 급격히 하락하기는 했지만, 여전히 Chrome과 Edge에 이은 3위의 자리에서 5.85%라는 무시할 수 없는 비중을 차지하고 있습니다. ([출처](https://gs.statcounter.com/browser-market-share/desktop/south-korea/#monthly-202106-202106-bar))

일정 비율의 사용자가 있는 이상 IE에 대한 크로스 브라우징은 필수였고, IE 버전별로 어떤 CSS가 지원되는지, 자바스크립트 명령어나 라이브러리가 오류가 나지는 않는지 일일이 확인하며 IE 전용 코드를 별도로 제작하거나 트릭을 쓰는 등의 작업은 웹 개발자에게 많은 인내와 시간을 요구했습니다.

<br>

## 무엇이 달라질까

더이상 IE를 지원하지 않아도 된다면 무엇이 달라질지, 일반적인 관점에서 가볍게, 데이블 위젯의 관점에서 좀 더 구체적으로 상상해봤습니다.

### 일반적인 관점

1. 커뮤니케이션

   IE 버전별 사용률을 확인하고, 지원 여부와 범위에 대해 누군가를 설득해야만 하는 상황이 없어질 것입니다.

2. 개발

   caniuse.com에 들어갈 일이 현저히 줄어들 것입니다. 모든 브라우저의 호환성을 볼 수 있다고는 하지만 IE 지원 여부를 확인하는 목적이 가장 컸기 때문이죠. babel과 webpack으로 지원했던 자바스크립트와, `-ms-`가 잔뜩 붙은 vendor prefix나 트릭을 통해 지원했던 CSS 작업에서도 고민이 줄어들 것 같습니다. [IE 버전별 CSS hack](https://css-tricks.com/how-to-create-an-ie-only-stylesheet/)을 추가해야 했던 방식도 먼 과거의 이야기가 되겠죠.

3. QA

   가장 많은 리소스가 투입됐던 IE 버전별 QA 단계가 줄어들 것이고, 만약 IE에 최적화된 사이트를 디버깅하거나 QA를 진행하더라도 실제 IE가 아닌 Edge 브라우저의 IE모드를 활용하게 될 것입니다. 물론 이것도 2029년까지지만요.

### 데이블 위젯의 관점

현재 데이블 위젯은 기능은 IE7, 디자인은 IE10 이상을 지원하고 있습니다. IE를 지원하지 않아도 된다면 여러 측면에서 변화가 생길 것입니다.

1. CSS

   먼저, 사용 가능한 CSS 범위가 확장된다는 것이 가장 큰 변화일 듯합니다.
   `flex/grid`, `line-clamp`, `css variables`, `calc`, `object-fit` 등 최선의 CSS가 IE에서 지원되지 않아 대안으로 적용하다 보니 불필요한 CSS가 추가되었던 케이스, 이미 쓰고는 있지만 크로스 브라우징을 위해 별도의 트릭을 추가해야 했던 케이스도 점점 사라질 것입니다. 더 간결하게 동작하기 때문에 에러를 방지할 수 있고 유지보수비용도 절감할 수 있습니다.

2. 웹폰트

   간혹 웹폰트로 매체의 폰트를 지원해야 하는 경우가 있습니다. 브라우저마다 지원하는 폰트 포맷이 달라 eot, svg, ttf, woff, woff2까지도 지원해야 했는데, IE 구버전을 위해 지원했던 eot 포맷을 믿고 거를 수 있게 됩니다.

   <img src="/techblog/assets/images/IE-Retirement/webfont-format.png" alt="브라우저별 웹폰트 지원 포맷" />
   <small style="display:block;text-align:right">출처) [w3schools.com](https://www.w3schools.com/Css/css3_fonts.asp)</small>

3. 이미지

   위젯에서 가장 중요한 요소라고 할 수 있는 섬네일에 차세대 이미지 포맷을 지원하기 위한 고민 역시 줄어들 것입니다.
   대표적인 최신 이미지 포맷인 AVIF 혹은 WebP를 지원하기 위해서는 브라우저 호환성을 고려해 `<picture>` + `<source srcset>`에 IE를 위한 fallback `<img>` 태그까지 작성해야 합니다.
   IE를 고려하지 않아도 된다면, 모던 브라우저만을 기준으로 더욱 빠르게, 저비용으로 고압축률의 섬네일을 제공할 수 있습니다. (BigSur OS 이하의 Safari 브라우저에 대한 별도의 대응은 필요합니다.)

   <img src="/techblog/assets/images/IE-Retirement/avif.png" alt="AVIF 포맷 브라우저별 호환성" />
   <small style="display:block;text-align:right">출처) [caniuse.com](https://caniuse.com/?search=avif) AVIF 호환성</small>

   <img src="/techblog/assets/images/IE-Retirement/webp.png" alt="WebP 포맷 브라우저별 호환성" />
   <small style="display:block;text-align:right">출처) [caniuse.com](https://caniuse.com/?search=webp) WebP 호환성</small>

4. 다크모드

   다크모드를 원하는 사용자가 늘어남에 따라 점점 다크모드를 지원하는 매체도 증가하고 있습니다. iframe이라는 데이블 위젯 특성상 사용자가 매체 사이트 안에서 toggle 형태로 직접 동작시키는 다크모드를 지원하기는 어렵습니다. 하지만 사용자 기기 자체에서 다크모드가 설정되어 있고 매체에서도 다크모드를 지원하는 경우라면 `prefers-color-scheme` 미디어쿼리를 활용해 다크모드에도 최적화된 위젯을 제공할 수 있습니다.

   <img src="/techblog/assets/images/IE-Retirement/prefers-color-scheme.png" alt="prefers-color-scheme 미디어쿼리 브라우저별 호환성" />
   <small style="display:block;text-align:right">출처) [caniuse.com](https://caniuse.com/?search=prefers-color-scheme)</small>

<br>

## 마치며

함께 한 시간이 길었던 만큼 IE를 지원해야만 했던 개발 조건에 너무 익숙해져서, IE 없는 환경에 적응하려면 우리에게도 노력과 시간이 필요할 것 같습니다. 이 글을 통해 IE와의 추억을 짧게나마 떠올려보고, 내년 6월 혹은 2029년의 변화에 대한 대처를 미리 준비하고 고민하는 시간이 되셨길 바랍니다. IE의 은퇴를 진심으로 축하합니다.

<hr>

## 참고 자료

- [Internet Explorer 11 desktop app retirement FAQ](https://techcommunity.microsoft.com/t5/windows-it-pro-blog/internet-explorer-11-desktop-app-retirement-faq/ba-p/2366549)
- [What is Internet Explorer (IE) mode?](https://docs.microsoft.com/en-us/deployedge/edge-ie-mode)
- [Today, the Trident Era Ends](https://schepp.dev/posts/today-the-trident-era-ends/)
- [What To Expect When You're Expecting To Drop IE11](https://dev.to/samthor/what-to-expect-when-you-re-expecting-to-drop-ie11-ifg)
- [The Revenge of the IE Box Model?](https://www.jefftk.com/p/the-revenge-of-the-ie-box-model)
- [왜 웹 개발자들은 익스플로러를 싫어하나요?](https://www.youtube.com/watch?v=T8r-6mMlzWg)
