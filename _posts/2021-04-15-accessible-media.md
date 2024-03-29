---
layout: post
title: 언론사 웹 사이트가 데이블을 만나면
date: 2021-04-15 07:00:00 +0900
author: Goonoo Kim
tags: [ Web, media, SEO, 웹 접근성 ]
---

여러분은 인터넷에서 뉴스를 읽으실 때 어디서 읽으시나요? 아마도 네이버나 다음 같은 포털에서 읽으시는 분들이 많으리라 생각합니다. 단순히 편해서 혹은 원래 가는 사이트라서 등 특별한 이유 없이 포털을 고르신 분들도 계시겠지만, 언론사 사이트가 불편하기 때문에 포털을 찾아가는 분들도 많다고 생각합니다.

이 글에서는 이런 언론사 사이트의 문제, 특히 혼란스러운 광고에 초점을 맞추어 이런 문제를 개선해 나아갈 수 있도록 노력하는 데이블의 접근을 살펴보려고 합니다. HTML5 API, SEO, 웹 접근성 등 기술적 내용이 포함됩니다.

## 언론사 웹 사이트에서 뉴스 읽기?

포털이 아닌 언론사 웹 사이트에서 뉴스를 읽는 경험을 해보신 분들 중 많은 분이 불편한 사용성을 이야기합니다. 특히 곳곳에 덕지덕지 붙은 광고는 뉴스를 가리기도 하고 번쩍이기도 하고 그 자체로 페이지의 로딩 속도를 저하합니다.

{% include figure_img.html url="/techblog/assets/images/accessible-news/1.jpg" alt="광고가 덕지덕지 붙어 불편한 뉴스 페이지 모바일 스크린샷" description="어떻게 콘텐츠를 읽어야 할지 난감한 모습" %}

언론사 입장에서는 뉴스 사이트를 운영하는 비용의 상당수를 온라인 광고의 매출을 통해 충당하고 있는데요. 더 많은 매출을 위해 광고를 늘렸는데, 이게 사용자들을 불편하게 만들어 떠나게 만들고, 그로 인해 줄어든 매출 때문에 광고를 또 늘리는 악순환의 고리가 이런 문제를 더욱 가속합니다.

## 언론사에 광고 다는 스타트업

데이블은 관련 기사, 개인화 기사 등 사용자들에게 편의를 제공하는 뉴스 추천 플랫폼으로 언론사와 접점을 만들며 2015년부터 언론사와 공생 관계를 이어오고 있는데요. 2016년부터는 여기에 광고를 얹어 사용자의 편의와 수익 창출 두 마리의 토끼를 잡는 플랫폼으로 진화해왔습니다.

언론사의 사용자들이 점차 줄어드는 문제는 데이블에게도 큰 위협이었습니다. 많은 광고 회사들이 당장의 이윤 추구를 위해 화면을 가리거나 사행성 내용을 담은 광고 등을 쏟아내고 있었고, 당장 매출을 올릴 수 있다는 사실이 여러 데이터를 통해 검증된 이런 광고의 도입을 놓고 데이블 안에서도 많은 고민이 있었습니다.

하지만 사용자에게 불편을 가중하는 결정이 장기적으로 가져올 결론은 줄어든 사용자와 매출이라는 생각을 했고, 사용자들이 뉴스를 보기 더 편하게 만드는 게 결국 데이블도 장기적으로 발전할 수 있는 길이라는 판단을 했습니다.

## 데이블이 거부하는 사용자를 괴롭히는 광고

그럼 구체적으로 데이블이 문제라고 판단하고 금지하고 있는 광고의 유형들을 살펴보겠습니다.

### 콘텐츠를 가리는 광고

뉴스 페이지 로딩이 완료되면 사용자는 PC에서는 보통 마우스 휠이나 키보드 아래 화살표 키, 모바일에서는 한 손가락 쓸어올리기, 즉 스크롤 기능을 통해 뉴스를 읽습니다. 뉴스를 읽기 전 혹은 도중 콘텐츠를 가리는 광고를 만나면 스크롤 동작 대신 뉴스를 읽기 위해 콘텐츠를 가리는 광고의 보통은 아주 작은 닫기 버튼을 클릭해야 합니다. 예상했던 스크롤 동작 대신 닫기 버튼 클릭이라는 동작을 수행해야 하는 점, (특히 모바일에서) 정확히 닫기 버튼을 클릭하지 못해 광고 페이지로 이동해버리는 점 등 많은 불편함이 야기되는 광고 유형입니다.

{% include figure_img.html url="/techblog/assets/images/accessible-news/1.jpg" alt="광고가 덕지덕지 붙어 불편한 뉴스 페이지 모바일 스크린샷" description="콘텐츠를 읽기 위해 몇개의 닫기 버튼을 실수 없이 눌러야 할까요?" %}

이 불편함은 특히 마우스 없이 키보드만 사용하는 사용자에게 치명적입니다. 마우스를 이용하면 닫기 버튼에 마우스 커서를 이동하여 바로 클릭하여 닫을 수 있지만, 웹 페이지의 링크, 버튼 등 초점을 받을 수 있는 요소를 순차적으로 탐색하는 키보드 사용자는 콘텐츠를 가리는 광고의 닫기 버튼에 초점을 이동하기 위해 반복하여 탭키를 눌러야 하고, 광고를 닫은 후에도 뉴스 본문의 링크 클릭 등을 위해 다시 뉴스 본문 영역까지 탭키를 반복적으로 눌러 이동해야 하는 상황에 부닥치게 됩니다.

### 뒤로 가기 시 광고 노출

SNS 등 외부링크를 통해 뉴스 링크를 클릭해서 본 후 이전 페이지로 돌아가기 위해 뒤로 가기 버튼을 눌렀는데 이전 페이지 대신 광고를 노출하는 경우입니다. 광고 업계에서는 이런 광고를 "캐치백 광고"라고 부릅니다. 캐치백 광고는 사용자에게 혼란을 유발합니다. 뒤로 가기 버튼을 눌렀을 때 사용자는 이전에 보던 페이지가 표시될 것을 기대하지만, 기대와 다른 콘텐츠 - 즉, 광고가 표시되기 때문입니다.

{% include figure_img.html url="/techblog/assets/images/accessible-news/2.png" alt="언론사 페이지에서 광고 클릭 후 광고 페이지로 이동했다가 뒤로 가기 버튼을 클릭했을 때 다른 광고가 노출되는 캐치백 광고" description="뒤로 가기를 했는데 느닷없이 광고를 보게 되신 경험 한 번쯤 있으시죠?" %}

특히 이 혼란은 시각장애인 사용자에게 치명적입니다. 화면 낭독기라는 웹 페이지를 음성으로 읽어주는 프로그램을 사용하는 시각장애인 사용자에게는 뒤로 가기 버튼을 눌렀을 때 광고가 읽어주는 상황을 만나면 뒤로 가기라는 동작이 정상적으로 수행된 것이 맞는지, 원래의 이전 페이지로 돌아가기 위해 어떤 동작을 취해야 하는지 등 상황 파악이 비시각장애인 사용자에 비해 어렵기 때문입니다.

### 번쩍이는 광고

사용자의 시선을 끌기 위해 배경색이 번쩍거리는 등 강렬한 시각 효과를 사용하는 광고가 있습니다. 이런 광고는 단순히 주의를 분산시키는 불편함을 넘어 간질 등의 장애가 있는 사용자에게 발작을 유발할 수 있는 위험한 광고입니다.

{% include figure_img.html url="/techblog/assets/images/accessible-news/3.jpg" alt="번쩍이는 광고 예시" description="현란한 색을 사용한 광고 배너 이미지가 네온싸인처럼 반짝입니다." %}

## 더 나은 광고, 더 나은 뉴스 읽기 환경을 위한 데이블의 노력

데이블은 사용자를 괴롭히는 광고의 금지를 넘어 아래와 같은 기술적 장치들로 쾌적한 뉴스 읽기 환경을 조성하고 있습니다.

### 페이지 로딩을 방해하지 않는 광고

웹 페이지에 광고를 추가하기 위해 광고 회사는 언론사에 `<script>` 나 `<iframe>` 태그로 이루어진 작은 코드 조각을 전달하고 언론사는 이 코드 조각을 뉴스 페이지의 특정 위치에 삽입하여 광고를 노출합니다. 이 태그들은 광고 회사가 운영하는 서버로 노출할 광고 데이터를 요청하는데, 광고 회사 서버가 응답이 늦거나 비정상적으로 동작하는 경우 언론사의 웹 페이지의 렌더링이 멈추는 등의 문제가 발생하기도 합니다.

`<script>` 태그에 `async` 혹은 `defer` 속성을, `<iframe>` 태그에 `loading="lazy"` 속성을 추가하여 광고의 로딩을 지연시킴으로써, 뉴스 콘텐츠의 렌더링을 빠르게 유지할 수 있습니다.

```
<script>
(function(d,a,b,l,e,_) {
if(d[b]&&d[b].q)return;d[b]=function(){(d[b].q=d[b].q||[]).push(arguments)};e=a.createElement(l);
e.async=1;e.charset='utf-8';e.src='//static.dable.io/dist/plugin.min.js';
_=a.getElementsByTagName(l)[0];_.parentNode.insertBefore(e,_);
})(window,document,'dable','script');
dable('setService', 'dable.io');
dable('sendLogOnce');
</script>
```
`async` 속성이 추가되어 지연 로딩되는 데이블 스크립트 예시

### SEO에 도움을 주는 광고

데이블은 추천 제공을 위해 기사 제목, 섬네일, 본문 등의 정보를 수집/분석합니다. 이를 위해 수집 과정을 단순히 언론사와 데이블 사이에 특정한 규칙을 만들기보다 뉴스 웹 페이지가 [Open Graph protocol](https://ogp.me/), [Schema.org](https://schema.org/) 등을 따라 시맨틱 마크업을 하면 그 메타 데이터에 따라 정보를 수집하도록 구성하여 검색 엔진 최적화(SEO), 웹 접근성 향상 등의 도움을 주고 있습니다.

{% include figure_img.html url="/techblog/assets/images/accessible-news/4.png" alt="기사 카테고리, 작성일, 본문 영역 등의 시맨틱 정보 추가를 안내하는 데이블 서비스의 화면 예시" description="데이블 서비스를 이용하려는 언론사는 기사 카테고리, 작성일, 본문 영역 등 다양한 시맨틱 정보를 추가해야 합니다." %}

### 데이터 다운로드를 최소화하는 광고

화면 밖의 큰 이미지의 다운로드를 방지하는 기술은 특히 웹툰 서비스 등에서 많이 쓰입니다. ([IntersectionObserver를 이용한 이미지 동적 로딩 기능 개선 - 레진 기술 블로그](https://tech.lezhin.com/2017/07/13/intersectionobserver-overview))

데이블도 [IntersectionObserver](https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API) 등의 API를 통해 사용자의 브라우저 화면에 노출되기 전까지 추천/광고 이미지의 로딩을 지연하여 데이터 다운로드 최소화 및 더욱 빠른 페이지 로딩을 지원합니다.

### seamless한 광고

데이블의 추천/광고를 포함한 "위젯"은 언론사 페이지의 다른 UI와의 이질감이 없도록 만들어집니다. 이렇게 만든 광고가 성능도 물론 좋지만, 사용자가 뉴스를 읽는 경험을 방해하지 않겠다는 데이블의 의지가 반영된 결과입니다. 물론, 이렇게 매끄러운 위젯을 만들기 위해 플랫폼에 더 많은 기능이 필요하고 기능이나 성능에 문제가 없이도 UI를 정교하게 다듬어야 하지만 이 운영 비용이 만들어내는 가치를 지지합니다.

## 앞으로 

데이블은 모든 언론사 사이트가 기술 회사인 네이버/다음에도 사용성과 성능이 뒤처지지 않게 되기를 바랍니다. 국내 언론사 외에도 대만/인도네시아/베트남/터키 등 데이블이 진출한, 또 진출할 국가의 언론사에도 마찬가지입니다. 단순히 건강한 광고 생태계를 만드는 것을 넘어 언론사 사이트와 최신 기술 사이의 간극을 더 적극적으로 메워가는 역할을 할 예정입니다.
