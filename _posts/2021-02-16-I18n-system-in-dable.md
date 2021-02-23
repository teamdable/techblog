---
layout: post
title:  "Dable의 다국어 지원(i18n) 시스템"
date:   2021-02-16 08:00:00 +0900
author: Woongki Kim
tags: [ 김웅기, i18n, 다국어, 국제화 ]
---

안녕하세요! Dable 광고플랫폼 개발팀의 i18n system 담당자 김웅기입니다.

Dable은 현재 한국 이외에도 대만, 말레이시아, 인도네시아, 베트남 등 다양한 국가에 서비스를 제공하고 있습니다.  
따라서 원활한 서비스를 위해서는 언어, 통화 등을 현지화하여 제공해야 합니다.  
이번 글에서는 현지화를 위한 여러 요소 중 다양한 언어를 제공하기 위한 다국어 시스템(i18n system)을 어떻게 구축하여 사용하고 있는지 소개하려고 합니다.

## i18n
이후로도 계속해서 등장할 **i18n**이라는 용어에 대해서 먼저 살펴보고 넘어가도록 하겠습니다.  

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
국제화를 [위키피디아](https://ko.wikipedia.org/wiki/%EA%B5%AD%EC%A0%9C%ED%99%94%EC%99%80_%EC%A7%80%EC%97%AD%ED%99%94)에서 검색하면 **국제화와 지역화**라고 하여 지역화라는 용어를 같이 다루고 있는 것을 볼 수 있습니다. 위키피디아의 설명은 이렇습니다.

> 국제화와 지역화는 출판물이나 하드웨어 또는 소프트웨어 등의 제품을 언어 및 문화권 등이 다른 여러 환경에 대해 사용할 수 있도록 지원하는 것을 의미한다. 이때 국제화는 제품 자체가 여러 환경을 지원할 수 있도록 제품을 설계하는 것을 의미하며, 지역화는 제품을 각 환경에 대해 지원하는 것을 의미한다.

위키피디아에서는 **번역**을 L10n의 요소로 이야기합니다. 저는 대체적으로 위키피디아의 설명에 공감합니다. 제품이 여러 환경을 지원할 수 있도록 제품을 설계하고 제작하는 것 자체는 **i18n**의 영역이고, **L10n**은 조금 더 구체적으로 지역을 한정하여 해당 지역의 언어, 문화적 특성을 고려하는 작업이라고 생각합니다. 
따라서 번역을 제공하는 것이 가능하도록 시스템을 구축하는 작업은 i18n으로 분류하고, 특정 지역의 언어로 번역을 만드는 일은 L10n으로 분류하는 것이 좋다고 생각합니다.
다만 Dable에서는 용어를 굳이 구분하지 않고 i18n을 **번역시스템 + 번역**을 함께 일컫는 용도로 사용하고 있으며, 이후에도 글에서 i18n이라는 단어가 나온다면 같은 의미로 생각하시면 되겠습니다.

<br>
## i18next
i18next는 JS로 작성된 i18n 프레임워크입니다([공식홈페이지](https://www.i18next.com/)). 위에서 i18n에서 고려해야 할 사항을 다섯 가지 정도로 말씀 드렸는데, 그 중 다섯번째인 **문자열 치환 방법**에 해당합니다.
Dable에서는 i18next를 사용하여 번역을 제공하고 있습니다. i18next는 다양한 프레임워크와 언어(React, Vue, Angular, Express... 심지어 NodeJS 및 PHP 등)를 지원하고 있기 때문에
서비스 별, Repository 별로 사용하는 프레임워크가 상이한 Dable에서 사용하기 알맞은 도구입니다.
  
오늘 포스팅의 주된 주제는 Dable의 i18n system에 대한 설명이기 때문에 사용법은 간단하게만 짚고 넘어가겠습니다. 모든 예시는 i18next 홈페이지에서 가져왔습니다.
i18next를 사용하기 위해서는 당연히 번역이 필요합니다(!). Resource라고 표현할 수도 있습니다. Resource는 아래와 같은 JSON 형태로 제공합니다.

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
`init()`의 다양한 옵션에 대해서는 [여기](https://www.i18next.com/overview/configuration-options)를 참조하세요.
  
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

<img src="/techblog/assets/images/dable-i18n/dable-i18n-system.png" alt="데이블의 i18n 시스템 구조를 그린 도표. i18n dashboard라는 서비스에 데이터베이스, AWS S3 저장소, Redis Elasticache 등의 서비스가 연결되어서 번역키의 배포를 위해 사용되고, 각 서비스 repository는 배포 과정에서 i18n-dashboard와 상호 작용하며 번역키의 수정, 추가, 삭제를 적용하고 동기화한다.">

요소가 많아서 그림이 잘 보이지 않을 것 같아서 간단히 풀어서 설명해 보겠습니다. Dable i18n system의 핵심은 **i18n-dashboard**입니다. 이미지의 한 가운데에 자리하고 있습니다.
이 대시보드는 
1. 번역키의 추가, 삭제 및 수정(AWS RDS에 저장)
2. 번역키를 json 파일로 만들어(snapshot) S3에 저장하고, 필요할 때는 snapshot 파일을 조회
3. RDS에 들어있는 번역키를 전부 Elasticache(Redis)에 저장 (현재는 매 10분 주기로 진행)
4. 주기적으로 번역 상황을 slack message로 알림
5. 번역가 및 해외 Dabler들이 직접 번역을 올릴 수 있도록 UI 제공(React + Redux)
6. 번역이 수정된 PR이 올라온 경우 **영어** 번역이 모두 완료되었는지 확인하여 PR approve  

등 다양한 역할을 수행하고 있습니다. 각 역할의 자세한 내용은 이후 더 설명하겠습니다.  
  
**i18n-sync**는 배포 과정 중에 **i18n-dashboard**와 상호 작용하여 번역키의 변경을 동기화하는(실제로는 i18n-dashboard에 요청을 보내는) 모듈입니다. Dable 내부 private repository 중 하나이며, 각 서비스에는 `package.json`에 추가되어 모듈 형태로 사용하고 있습니다.  
  
이어서 Dable이 번역키(Resource)를 어떻게 관리하는지 설명하고 그 후에 서비스 배포 과정에서의 i18n을 설명하도록 하겠습니다.
  
### Dable의 번역키 관리
기본적으로 **한국어** 번역을 기준으로 번역키 관리를 합니다. 각 서비스의 repository에서는 한국어 번역키 파일만 관리하고, 그 외의 외국어 키는 i18n-system을 통해 관리한다고 보시면 됩니다.
외국어 키는 배포 과정에서 추가되며, live server의 local에 file로 저장되어 서비스에 번역키를 제공하게 됩니다. 그럼 한국어 번역키 파일의 형태를 보겠습니다.
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
배포 과정에서 i18n-sync 모듈이 작동하여 Database에서 외국어 번역키를 모두 가져오게 되고, 언어별로 `locales`폴더 아래에 각 언어의 코드를 폴더명으로 하여 저장됩니다. 
동시에 i18n-sync 모듈이 `/locales/index.js` 파일을 새로 추가된 번역키들을 import 하도록 다시 씁니다. 
그리고 최종 live 배포가 이루어져서 서비스의 웹 서버가 켜질 때, 모든 번역 파일을 하나의 파일로 묶은 `public/dist/locale/translation.js` 파일을 만들고, 해당 파일을 제공하게 됩니다.(이건 모든 서비스가 그렇지는 않고, 각 서비스의 특성에 맞춰 조금 다르게 적용된 곳도 있습니다)

그럼 이제부터 배포 과정을 차례로 짚어보며 i18n-system이 어떻게 흘러가는지 조금 더 자세히 살펴 보겠습니다. Dable의 번역키 관리 방식에 대한 설명이 조금 미흡하게 느껴지셨더라도, 배포 과정에서 보충이 되리라 생각합니다.
<br>
  
### 배포 과정
Dable에서는 Github과 Jenkins를 이용하여 서비스를 배포합니다. 이 배포 과정을 Pull Request, Merge & Build, Build의 세 단계로 나누어 각 단계에서 i18n이 어떻게 동작하는지 설명을 해보겠습니다.  

#### Pull Request
<img src="/techblog/assets/images/dable-i18n/i18n-process-pr.png" alt="데이블의 i18n 시스템이 동작하는 프로세스를 나타낸 그림. github에 Pull Request를 올렸을 때 어떤 일이 일어나는지 그리고 있다. PR이 올라온 브랜치에 번역키가 추가된 내용이 있으면 DB에 추가하고 영어 번역 상태를 체크한다. 영어 번역이 완료된 경우 PR을 승인한다.">
첫 번째로 Pull Request 단계를 설명하겠습니다. 개발자가 작업한 feature 브랜치를 merge하기 위해 PR을 올리면 Github webhook을 통해 Jenkins Job이 실행됩니다. 준비된 Test를 돌리고 Test가 통과하면 i18n-sync 객체가 동작합니다. 
i18n-sync 객체는 새로 추가된 번역키가 있으면 해당 key 정보를 i18n-dashboard에 post하여 Database에 등록할 수 있도록 합니다. merge까지 실제로 이어질 것인지 확신할 수 없기 때문에 추가된 번역키에 대해서만 작업을 하게 됩니다. 이후 추가된 번역키 내역을 번역 담당자가 확인하여 번역할 수 있도록 지정된 slack 채널에 전송합니다.
번역 담당자는 i18n-dashboard의 ui를 이용하여 번역을 등록합니다.  
  
최초로 PR를 등록할 때 한 번(번역키 수정이 없는 경우 Test만 통과하면 PR approve를 해주기 위함), 그리고 그 이후 영어 번역 키가 i18n-dashboard에 등록될 때 영어 번역이 모두 완료 되었는지 확인합니다. 다양한 언어로 서비스가 제공되지만 영어 번역이 완료되면 서비스를 내보낼 수 있다고 판단하고 dable-bot이 PR을 approve합니다.
여기까지 진행이 되었다면 merge를 위한 준비가 끝나게 됩니다. QA팀의 검수를 위해 특정 branch를 지정하여 서버를 띄우는 과정이 있긴 하지만, i18n system과는 크게 연관이 없어 생략하도록 하겠습니다.


#### Merge
이제 Pull Request가 Merge된 후 Build가 일어나기 전까지의 과정을 설명하겠습니다. 번역이 필요한 Dashboard류의 서비스들은 대부분 Docker Image Build까지 한 호흡으로 일어나지만, 편의상 build 전까지의 작업만 먼저 설명 하겠습니다. 흐름은 다음과 같습니다.  
<img src="/techblog/assets/images/dable-i18n/i18n-process-merge.png" alt="i18n 시스템의 merge 과정을 나타낸 그림. 풀 리퀘스트가 merge되면 번역키의 브랜치 정보도 모두 master로 변경하고 삭제된 키를 지운 후에, 현재의 번역키 전부를 json 형태로 s3에 저장한다.">  
  
Pull Request가 merge되고, 브랜치가 삭제되면(저희는 merge된 branch를 자동으로 삭제하도록 옵션을 설정해 두었습니다) webhook을 통해 Jenkins Build Job이 실행됩니다. 그럼 i18n-sync 객체의 merge 메소드가 실행됩니다.
내용은 단순합니다. DB에 등록된 번역키는 branch 값이 같이 저장되어 있는데요, PR을 올릴 때 새로 추가된 키는 feature 브랜치명이 들어가 있습니다. 그래서 merge된 브랜치 명으로 키를 검색하여 해당 row의 branch 값을 **master**로 변경해줍니다.
그리고 PR에서 삭제된 번역키가 있다면 이 단계에서 실제 키를 삭제합니다. 그리고 key 삭제 알람을 슬랙으로 전송합니다.  
  
그 이후 현재 DB에 저장되어 있는 (해당 서비스의)번역키를 모두 JSON 형태로 만들어서 S3에 저장합니다. 이를 저희는 snapshot이라고 부릅니다. 파일 이름은 서비스 이름과 스냅샷의 버전을 조합하여 만들어집니다. i18n DB에는 각 서비스별로 스냅샷을 몇 개 가지고 있을지, 가지고 있는 스냅샷이 어떤 버전인지를 기록해 두었습니다.
따라서 새로 스냅샷을 추가하여 스냅샷 한도를 초과하였다면 가장 오래된 스냅샷 하나를 지웁니다. 여기까지 완료되었다면 이후에는 Image build를 시작합니다. 
  
#### Build
배포 과정의 마지막 단계로 Build 과정을 설명드리겠습니다. Build 과정은 간단하여 별도로 그림을 첨부하지 않고 글로 설명하도록 하겠습니다. 
merge를 설명할 때 merge와 build는 편의상 나눠서 설명을 드렸지만 실제 Jenkins에서는 하나의 Job 내부에서 같이 실행됩니다. Build 직전에 만든 스냅샷의 버전을 환경 변수로 넣어서 Docker Image Build가 일어납니다.
```dockerfile
# DABLE I18N VERSION
ARG I18N_VERSION
ENV I18N_VERSION ${I18N_VERSION}

## BUILD
RUN npm run lang:refresh -- --i18n_version=$I18N_VERSION
```
`npm run lang:refresh` 커맨드는 i18n-sync의 localSync 메소드를 실행합니다. 이때 전달받은 snapshot의 version을 parameter로 같이 넘기게 됩니다. 
localSync 함수는 snapshot version을 전달받으면 S3 bucket에서 해당 스냅샷을 조회하여 번역키를 불러옵니다. 그리고 불러온 번역키를 `/locales/` 폴더 안에 국가별로 나누어서 저장해둡니다.
그리고 Build한 이미지는 AWS 이미지 저장소에 저장합니다.  
  
지금까지 배포 과정에서 번역키가 관리되는 흐름을 정리해봤습니다. 다음은 마지막 순서로 live server에서는 i18n system이 어떻게 동작하는지 보겠습니다.  
  
### Live
<img src="/techblog/assets/images/dable-i18n/i18n-process-live.png" alt="live server에서 i18n system이 동작하는 구조를 나타낸 그림. i18n-dashboard는 10분마다 Redis에 번역 키 전체를 밀어넣고, 각 서버는 1분마다 레디스를 확인하여 번역키에 수정이 생겼으면 키를 받아와서 수정함. 그리고 i18n-dashboard는 매 월요일마다 번역이 완료되지 않은 서비스의 번역 현황을 퍼센트로 계산하여 슬랙에 전송한다.">
빌드된 Docker Image를 가져다가 live server를 켤 때, `/locales/` 폴더 내부에 언어별로 찢어져 있는 번역 파일을 모두 모아서 하나로 만들어 `public/dist/locale` 폴더에 넣습니다.
그리고 그 이후 다른 언어의 번역키가 추가되거나, 기존의 번역키가 수정된 경우를 위해 주기적으로 동기화 작업을 실행합니다. 동기화 작업은 총 3 부분으로 나누어 볼 수 있습니다.

1. key_sync  
i18n-dashboard는 10분 마다 모든 서비스의 번역키를 DB에서 가져와서 Dable 내부에서 공용으로 사용하는 Elasticache(redis)에 집어넣습니다. Redis에 넣을때의 Key는 서비스명과 번역키명 등을 조합하여 규칙적으로 만들어집니다. 

2. reload  
각 서비스는 1분 마다 i18n-dashboard에 서비스 가능한 언어 목록을 요청합니다. 서비스 가능한 언어 목록은 현재 서비스에 등록된 번역키의 언어 값을 `DISTINCT`하여 받아오는 값입니다. 
위에서 언급한 Redis에서 번역키를 전부 받아와서 서비스 가능한 언어 별로 local파일과 비교하여 달라진 점을 체크합니다. 이때 달라진 점이 존재한다면 달라진 부분을 갱신하여 translation.js 파일을 새로 만듭니다.

3. slack_reminder
i18n-dashboard에서 매주 월요일 오후 3시에 실행됩니다. 서비스(그림에 나온 RECO, MKT는 저희 대시보드중 가장 많이 쓰이는 서비스입니다)의 번역 현황을 계산하여 퍼센트로 나타낸 후 슬랙에 전송하여 아직 번역을 못한 담당자들이 잊고 넘어가지 않도록 돕습니다.
  
Live server에서의 i18n system을 살펴보았습니다. 배포 과정과 Live 과정의 동작을 설명함으로 Dable의 i18n 시스템에 대한 전반적인 설명을 모두 마쳤습니다.

<br>
  
## 마치며
지금까지 i18n이 무엇인지, i18next는 또 무엇인지, Dable에서는 i18n 시스템을 어떻게 만들어 사용하고 있는지를 말씀드렸습니다. 혹시 서비스의 번역 시스템 도입을 고민하고 계셨던 분이 이 글을 보시고 조금이나마 도움을 얻으셨으면 좋겠습니다.
아직 Dable의 i18n 시스템도 완벽히 완성된 것이 아닙니다. 번역키 sync 과정 고도화, 번역 파일의 더욱 컴팩트한 서빙 등의 목표를 잡고 서비스를 개선할 예정입니다.   
앞으로 데이블이 진출한 국가가 많아지면 i18n도 변모할 일이 생길텐데 그 때 또 새로운 변경 사항을 가지고 포스팅으로 돌아오겠습니다.