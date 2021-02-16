---
layout: post
title:  "Dable의 다국어 지원(i18n) 시스템"
date:   2021-02-16 08:00:00 +0900
author: Woongki Kim
tags: [ 김웅기, i18n, 다국어, 국제화 ]
---

안녕하세요! Dable 광고플랫폼 개발팀의 김웅기입니다.

Dable은 현재 한국 이외에도 대만, 말레이시아, 인도네시아, 베트남 등 다양한 국가에 서비스를 제공하고 있습니다.  
따라서 원활한 서비스를 위해서는 언어, 통화 등을 현지화하여 제공해야 합니다.  
이번 글에서는 현지화를 위한 여러 요소 중 다양한 언어를 제공하기 위한 다국어 시스템(i18n system)을 어떻게 구축하여 사용하고 있는지 소개하려고 합니다.

## i18n
이후로도 계속해서 등장할 `i18n`이라는 용어에 대해서 먼저 살펴보고 넘어가도록 하겠습니다.  

> i18n === Internationalization(국제화)  
> i와 n 사이에 18개의 알파벳이 있다는 의미입니다.

i18n은 소프트웨어가(소프트웨어에 한정된 개념은 아니지만 여기서는 소프트웨어의 i18n으로 한정하여 이야기 하겠습니다) 특정 지역이나 언어에 종속되지 않고 다양한 지역과 언어 환경에서 정상 동작하도록 국제적으로 통용되는 소프트웨어를 설계하고 개발하는 과정을 말합니다.
따라서 i18n은 단순히 번역을 제공하는 것을 넘어 다음과 같은 여러 가지 사항을 고려해야 합니다.
1. 각 지역 언어의 인코딩 방식 - 유니코드, 쓰기 방향, 문자열 정렬 순서 등
2. 날짜/시간 형식, 달력, 통화
3. 번역 리소스 외부화 - 프로그램을 직접적으로 수정하지 않고 다국어 지원이 가능하도록 하기 위해
4. UI 대응(문자열 크기 변화, 폰트 등)
5. 문자열 치환 방법

<br>
#### i18n vs L10n(Localization)
국제화를 [위키피디아](https://ko.wikipedia.org/wiki/%EA%B5%AD%EC%A0%9C%ED%99%94%EC%99%80_%EC%A7%80%EC%97%AD%ED%99%94)에서 검색하면 `국제화와 지역화`라고 하여 지역화라는 용어를 같이 다루고 있는 것을 볼 수 있습니다. 위키피디아의 설명은 이렇습니다.

> 국제화와 지역화는 출판물이나 하드웨어 또는 소프트웨어 등의 제품을 언어 및 문화권 등이 다른 여러 환경에 대해 사용할 수 있도록 지원하는 것을 의미한다. 이때 국제화는 제품 자체가 여러 환경을 지원할 수 있도록 제품을 설계하는 것을 의미하며, 지역화는 제품을 각 환경에 대해 지원하는 것을 의미한다.

위키피디아에서는 `번역`을 L10n의 요소로 이야기합니다. 저는 대체적으로 위키피디아의 설명에 공감합니다. 제품이 여러 환경을 지원할 수 있도록 제품을 설계하고 제작하는 것 자체는 `i18n`의 영역이고, `L10n`은 조금 더 구체적으로 지역을 한정하여 해당 지역의 언어, 문화적 특성을 고려하는 작업이라고 생각합니다. 
따라서 번역을 제공하는 것이 가능하도록 시스템을 구축하는 작업은 i18n으로 분류하고, 특정 지역의 언어로 번역을 만드는 일은 L10n으로 분류하는 것이 좋다고 생각합니다.
다만 Dable에서는 용어를 굳이 구분하지 않고 i18n을 `번역시스템 + 번역`을 함께 일컫는 용도로 사용하고 있으며, 이후에도 글에서 i18n이라는 단어가 나온다면 같은 의미로 생각하시면 되겠습니다.

<br>
## i18next
i18next는 JS로 작성된 i18n 프레임워크입니다([공식홈페이지](https://www.i18next.com/)). 위에서 i18n에서 고려해야 할 사항을 다섯 가지 정도로 말씀 드렸는데, 그 중 다섯번째인 `문자열 치환 방법`에 해당합니다.
Dable에서는 i18next를 사용하여 번역을 제공하고 있습니다. i18next는 다양한 프레임워크와 언어(React, Vue, Angular, Express... 심지어 PHP)를 지원하고 있기 때문에
서비스 별, Repository 별로 사용하는 프레임워크가 상이한 Dable에서 사용하기 알맞은 도구입니다.
  
오늘 포스팅의 주된 주제는 Dable의 i18n system에 대한 설명이기 때문에 사용법은 간단하게만 짚고 넘어가겠습니다. 모든 예시는 i18next 홈페이지에서 가져왔습니다.
i18next를 사용하기 위해서는 당연히 `번역`이 필요합니다(!). Resource라고 표현할 수도 있습니다. Resource는 아래와 같은 JSON 형태로 제공합니다.

```json
{
    "key": "value of key",
    "look": {
        "deep": "value of look deep"
    }
}
```
Resource는 직접 static한 파일로 제공하는 것도 가능하고, 플러그인을 사용하여 데이터베이스와 연결하는 것도 가능합니다.
이후 더 설명을 드리겠지만, Dable은 배포 시에 프로젝트를 build 하면서 일차적으로 AWS S3에 저장된 json 파일을 통해 resource를 가져오고(저희는 snapshot이라고 부릅니다),
배포 이후의 변경 사항을 반영하기 위해서 Redis와 연결하여 번역 Resource를 가져옵니다. i18next는 mongodb, nodejs filesystem 등을 연결하는 플러그인을 제공하지만,
Redis와 연결하는 플러그인은 따로 없어서 저희가 만든 것을 사용하고 있습니다.

이렇게 Resource가 준비되면 i18next를 init하여 사용하기만 하면 됩니다.

```javascript
import i18next from 'i18next';

i18next.init({
  lng: 'en',
  debug: true,
  resources: {
    en: {
      translation: {
        "key": "value of key",
        "look": {
          "deep": "value of look deep"
        }
      }
    }
  }
}, function(err, t) {
  // initialized and ready to go!
  document.getElementById('output').innerHTML = i18next.t('key');
});

i18next.t('key');
// -> "value of key"
i18next.t('look.deep');
// -> "value of look deep"

```
`init`의 다양한 옵션에 대해서는 [여기](https://www.i18next.com/overview/configuration-options)를 참조하세요.
  
아래와 같이 다양한 플러그인을 추가하는 것도 가능합니다. languageDetector같은 플러그인은 아주 유용합니다.
언어를 queryString, cookie, path 등을 이용하여 찾아주기 때문에 Dable에서도 이용하고 있습니다. browser 뿐 아니라 다양한 환경에서 동작하는 플러그인이 있으니 확인해보세요! [(링크)](https://www.i18next.com/overview/plugins-and-utils#language-detector)

```javascript
import i18next from 'i18next';
import Backend from 'i18next-http-backend';
import Cache from 'i18next-localstorage-cache';
import postProcessor from 'i18next-sprintf-postprocessor';
import LanguageDetector from 'i18next-browser-languagedetector';

i18next
  .use(Backend)
  .use(Cache)
  .use(LanguageDetector)
  .use(postProcessor)
  .init(options, callback);
```
  
위의 예제를 합하여 Dable이 지금 사용하는 형태와 유사하게 만들어 본다면 아래와 같습니다.
```javascript
import i18next from 'i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

i18next
  .use(LanguageDetector)
  .init({
  debug: true,
  detection: { // languagedetector option
    order: ['querystring', 'htmlTag', 'cookie'], // detect 우선순위 
    lookupQueryString: 'lang', // ?lang=
    lookupCookie: 'i18n_lang' // cookie name
  },
  resources: {
    en: {
      translation: {
        "key": "value of key",
        "look": {
          "deep": "value of look deep"
        }
      }
    },
    ko: {
      translation: {
        "key": "이건 key에 대한 번역 value입니다.",
        "look": {
          "deep": "한 단계 더 들어간 deep value입니다."
        }
      }
    }
  }
}, function(err) {
  if(err) console.error(err);
});

i18next.t('key');
// -> 만약 lang이 'ko'라면 "이건 key에 대한 번역 value입니다."
```
같은 키에 대하여 각 언어로 번역한 resource를 제공하고, 브라우저에서 detector가 감지한 언어에 맞추어 번역이 제공되는 형태입니다. Dable에서도 일부 옵션 값은 다르지만 비슷한 형태로 사용하고 있습니다.
지금까지 i18next의 기본적인 사용법을 살펴보았습니다. 복수형 지원, 변수 사용 등 i18next에 대해 더 자세한 내용이 필요하신 분은 [i18next 공식 홈페이지](https://www.i18next.com/)의 공식 문서를 확인하시면 됩니다.  
<br>
이제 드디어 Dable의 i18n system에 대해서 설명하겠습니다.  
<br>
  
## Dable i18n System  

Dable은 다양한 서비스에서 사용되는 i18n의 번역키 관리, 배포를 용이하게 하기 위해 별도의 system을 구축하여 사용하고 있습니다. 다음에 나오는 이미지는 전체 구조를 간략하게 표현한 이미지입니다.

<img src="/techblog/assets/images/dable-i18n/dable-i18n-system.png" alt="dable i18n system architecture graph">

요소가 많아서 그림이 잘 보이지 않을 것 같아서 간단히 풀어서 설명해 보겠습니다. Dable i18n system의 핵심은 `i18n-dashboard`입니다. 이미지의 한 가운데에 자리하고 있습니다.
이 대시보드는 
1. 번역키의 추가, 삭제 및 수정(AWS RDS에 저장)
2. 번역키를 json 파일로 만들어(snapshot) S3에 저장하고, 필요할 때는 snapshot 파일을 조회
3. RDS에 들어있는 번역키를 전부 Elasticache(Redis)에 저장 (현재는 매 10분 주기로 진행)
4. 주기적으로 번역 상황을 slack message로 알림
5. 번역가 및 해외 Dabler들이 직접 번역을 올릴 수 있도록 UI 제공(React + Redux)
6. 번역이 수정된 PR이 올라온 경우 `영어` 번역이 모두 완료되었는지 확인하여 PR approve  

등 다양한 역할을 수행하고 있습니다. 각 역할의 자세한 내용은 이후 더 설명하겠습니다.  
  
`i18n-sync`는 배포 과정 중에 `i18n-dashboard`와 상호 작용하여 번역키의 변경을 동기화하는(실제로는 i18n-dashboard에 요청을 보내는) 모듈입니다. Dable 내부 private repository 중 하나이며, 각 서비스에는 `package.json`에 추가되어 모듈 형태로 사용하고 있습니다.  
  
이어서 Dable이 번역키(Resource)를 어떻게 관리하는지 설명하고 그 후에 서비스 배포 과정에서의 i18n을 설명하도록 하겠습니다.
  
### Dable의 번역키 관리
저희는 가장 기본이 되는 번역키를 `한국어` 번역이라고 생각을 하고, 한국어 번역을 기준으로 번역키 관리를 합니다. 각 서비스의 repository에는 한국어 번역 키만 직접 넣어서 관리하고, 그 외의 외국어 키는 i18n-system을 통해 관리한다고 보시면 됩니다.
추가되는 외국어 키는 배포 과정에서 추가되며, live server의 local에 file로 저장되어 번역키를 제공하게 됩니다. 그럼 한국어 번역키를 어떻게 관리하는지 보겠습니다.
```javascript
// /locales/ko/translation.js
export default {
  "nav": {
    "홈": "홈",
    "콘텐츠 관리": "콘텐츠 관리",
    "캠페인 관리": "캠페인 관리",
    "성과 분석": "성과 분석",
    ...
  }
}
```
대부분의 서비스가 locales 폴더를 만들어 그 안에 번역키 파일을 저장하도록 만들어져 있습니다. 
```javascript
// /locales/index.js
import translation_ko from './ko/translation';

const locales = {
  'ko': {
    translation: translation_ko,
  },
};

export default locales;
```



그럼 이제부터 배포 과정을 차례로 짚어보며 i18n-system이 어떻게 흘러가는지 살펴 보겠습니다.  
<br>
  
### 배포 과정

