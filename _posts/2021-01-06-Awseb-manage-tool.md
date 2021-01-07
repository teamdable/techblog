---
layout: post
title:  "서비스 비용 절감을 위한 Dable의 자체 AWS Elastic Beanstalk 관리 내부 tool 을 소개합니다"
date:   2021-01-06 15:00:00 +0900
author: Yoonji Oh
tags: [ 오윤지, AWS, Devops, 서버 ]
---

안녕하세요 Dable 광고플랫폼 개발자 오윤지입니다. 최근에 회사에서 담당하게 된 서비스인 Elastic Beanstalk(이하 EB) 관리 tool을 이번 글에서 소개하려 합니다. 

Dable 은 2015년부터 AWS Elastic Beanstalk service를 통해 EC2 서버들을 관리해오고 있습니다. 
2021년 1월 현재 실행중인 EB 환경과 그에 속한 인스턴스 개수는 각각 106개와 721개로, 소수의 개발자가 직접 관리할 수 있는 범위를 넘어선 지 오래되었습니다.
관리가 힘들어지는 것도 문제지만 늘어나는 서버비에 대한 고민이 컸는데요, 아마 이 점은 AWS EC2 서비스를 쓰고 있는 개발자분들이라면 다들 공감하실 것으로 생각합니다. 

서버비가 늘어나는 포인트에는 여러 가지가 (예: 불필요한 네트워크 비용 등) 있지만 이번에 소개할 Dable EB 관리 tool은 인스턴스 구매 타입에 초점을 둔 서비스입니다.
이 서비스의 목적은 "비싼 ONDEMAND 타입보다는 최대한 SPOT 타입 인스턴스를 구매해 사용하자" 입니다.

~~~
* SPOT 타입과 ONDEMAND 타입의 비용 차이 (* linux, 서울 region 기준)

c5.4xlarge의 ONDEMAND 요금 0.7680 USD
c5.4xlarge의 SPOT 요금 0.2397 USD

=> 같은 instance type이어도 ONDEMAND 요금이 3배 이상 비쌉니다.
~~~

### 핵심 아이디어
SPOT이 좋으면 그냥 AWS Auto Scaling Group (이하 ASG)의 Launch Configuration (이하 LC)을 SPOT 타입으로 설정해 해당 EB에서 새로 생성되는 인스턴스는 
자동으로 SPOT 타입으로 뜨게 하면 되지 않나? 왜 이를 위한 관리 tool이 따로 필요하지? 라고 생각하실 수 있습니다. 문제는 AWS의 탁월한 비즈니스 모델에 있습니다.
AWS는 ONDEMAND 보다 훨씬 저렴한 가격에 SPOT을 제공해 고객을 끌어모으는 대신, 해당 SPOT 타입이 인기가 많아 물량이 부족해지면 언제든 고객의 동의 없이 SPOT을 뺏어갈 수 있습니다. 
이러한 점은 서비스의 안정성 측면에서 치명적인 장애를 일으킬 수 있어 개발자는 항상 언제 SPOT을 뺏길지 불안해하는 상황에 처하게 됩니다. 

그래서 Dable은 EB 당 Launch Configuration을 SPOT 타입과 ONDEMAND 타입을 복수로 만들어 두고, 
Launch Configuration들의 우선순위를 정해 해당 순위 SPOT이 물량이 부족해 인스턴스들이 종료되기 전 ASG Launch Configuration을 다음 순위로 바꾸는 
방법을 사용해 SPOT 물량이 부족해 생기는 장애를 예방하면서도, 다음 순위의 SPOT으로 인스턴스를 띄워 비용 절감도 해보자! 라는 생각을 했습니다.

### Architecture
<img src="/techblog/assets/images/Awseb-tool/awseb-architecture.png" alt="EB Tool 아키텍처" width="800">

이러한 아이디어를 기반으로 설계된 데이블 내부 관리 tool의 아키텍처는 위와 같습니다.

1. AWS EventBridge 
AWS EventBridge는 고객이 알림 받고자 하는 이벤트를 EventBridge에서 고르면 해당 이벤트 발생 시 원하는 액션을 트리거할 수 있는 서비스입니다. 
위 아키텍처를 보시면 Spot instance Interruption warning, EB Managed Updates event 두 개를 받고 있습니다.

2. AWS lambda job
EventBridge에 등록한 이벤트 알람을 받을 시 실행되길 원하는 lambda job이 필요합니다. 
Spot instance Interruption warning이 발생하면 SpotInstanceMonitor job이 실행되고,
EB Managed Updates event가 발생하면 EBManagedUpdatesMonitor job이 실행됩니다. 
해당 job이 하는 일은 1) 각 이벤트가 발생한 인스턴스와 EB 환경 정보를 가져오고 2) 그 정보들을 Dable EB 관리 서버에 API 호출을 통해 알려주는 것입니다. 
lambda job과 EventBridge 간 관계 설정은 lambda job 설정에서 할 수 있습니다.

3. State Machine
Dable EB 관리 서버는 15초에 한 번씩 돌아가는 worker로 구성됩니다. 이 main worker가 돌 때마다 DB에서 모니터링 대상 EB 들을 가져온 후, 
각 EB들의 현재 state를 파악하여 state 별 worker를 실행시키는 구조입니다. 한 개의 main worker 안에 여러 개의 state worker 들이 독립적으로 실행되는 모양새입니다. 
State Machine 작동에 관해서는 아래에서 더 자세히 다루기로 하겠습니다.

4. AWS SDK
각 State worker에서 실행되는 함수들에서는 AWS api 들이 실행됩니다. instance와 EB의 정보를 가져오는 api, instance를 종료시키는 api, 
EB ASG (Auto Scaling Group)의 Launch Configuration을 바꿔주는 api 등입니다. 이러한 api 들을 AWS SDK를 설치하여 실행시킬 수 있습니다.

5. 관련 DB
두 가지 DB 테이블을 사용합니다.
    1) AWSEB_STATE_LOG
  각 EB 의 state 들이 언제 어떻게 바뀌었는지 로그를 남기는 테이블입니다. EB의 아이디, state, message, create_time 을 필드로 가집니다. 
    2) AWSEB_ENVIRONMENT
  각 EB 의 이름, 모니터링 여부, Launch Configuration 우선순위 등을 필드로 가집니다.
  
### UX와 State Machine

EB를 생성한 후 관리 tool client에서 모니터링을 시작한 후 아래 이미지와 같이 최대 3개의 Launch Configuration을 등록하고, 우선순위를 정합니다. 

<img src="/techblog/assets/images/Awseb-tool/awseb-ux.png" alt="EB Tool UX 이미지" width="800">

1순위와 2순위는 SPOT 타입으로, 3순위는 안정성을 위해 ONDEMAND 타입으로 하는 것을 권장합니다. 2순위의 SPOT 인스턴스 타입은 1순위보다 1세대 낮은 것을 선택해, 상대적으로 수요가 많은 1순위 SPOT의 물량이 없을 시 대체재로 쓰이도록 합니다. 2순위로 넘어간 후에는 쿨타임을 2시간 주는데, 2시간 이내에 2순위 SPOT조차 물량이 부족해진다면 3순위 ONDEMAND Launch Configuration으로 넘어가게 됩니다. 개발자들은 이러한 상태변화를 로그를 통해 확인할 수 있습니다.

<img src="/techblog/assets/images/Awseb-tool/awseb-state-flow.png" alt="EB Tool state 머신 플로우" width="800">

Dable 관리 tool에서 모니터링하고 있는 EB 들은 위 cycle을 거치게 됩니다. 어떤 EB의 상태가 SPOT_STABLE이라는 것은 해당 EB에 속한 모든 인스턴스의 타입이 SPOT이라는 의미이며, 
안정적으로 운영되고 있다 뜻입니다. 그런데 세 가지 상황에서 SPOT_STABLE은 다른 state로 넘어가게 됩니다. 

첫째, ASG Launch Configuration으로 등록된 SPOT 타입의 물량이 부족할 경우입니다. 1순위건 2순위건 상관없이, 이러한 경우 경고 이벤트가 온 
인스턴스들의 타입을 현재 ASG Launch Configuration와 비교하여 우선순위에서 몇 번째인지 체크한 후 다음 후보 Launch Configuration 타입을 파악하여 
그것이 SPOT 타입이면 `SPOT_REQUEST`로, ON DEMAND 이면 `ONDEMAND` state로 넘어가게 됩니다. `SPOT_REQUEST`에서는 새로운 SPOT 요청들이 성공했는지 체크하고, 
실패 시 SPOT_UNAVAILABLE로 넘어가 Launch Configuration을 바꾸는 작업을 반복합니다. ONDEMAND 상태에서는 ASG Launch Configuration를 
1순위로 바꾸고 쿨타임 2시간이 지나면 5분 간격으로 ONDEMAND 타입 인스턴스들을 EB로부터 1대씩 분리 및 종료시켜 인스턴스를 교체합니다.

둘째, ASG Launch Configuration의 우선순위가 2순위이고, 2시간의 쿨타임이 지나면 SPOT_ONREADY_FROM_2ND_SPOT 상태로 넘어갑니다. 
바뀐 상태에서 ASG Launch Configuration을 1순위로 다시 바꿔주고, 2순위인 인스턴스들을 5분에 한 대씩 분리 및 종료를 시켜 
1순위 Launch Configuration으로 새로 인스턴스들을 채웁니다. 이 작업은 떠 있는 인스턴스가 모두 1순위로 교체될 때까지 계속되며 모두 교체하면 다시 SPOT_STABLE로 넘어가게 됩니다. 

셋째, EB의 Managed Update가 실행된 경우입니다. 주기적으로 maintenance가 필요한 EB의 경우 EB Managed Update 기능을 사용하실 텐데요, 문제는 이 작업이 끝나면 ASG Launch Configuration이 ONDEMAND 타입으로 초기화된다는 점이었습니다. 그래서 AWS EventBridge 에서 Managed Update가 끝나면 오는 이벤트를 람다잡으로 받아 이를 알리는 api 를 호출하여 EB_UPDATE_FINISHED 상태로 바꾸어주어 첫 번째 Launch Configuration으로 바꾸는 코드를 추가하였습니다.

이와 같은 방법을 통해 Dable은 EB의 인스턴스 구매 타입 관리를 자동화하고 있습니다. AWS EB를 대량으로 사용하고 있는 경우에 이처럼 AWS api를 활용하여 
관리 tool을 만들어 사용하면 서버비 절감과 관리 편의성이라는 두 마리 토끼를 함께 잡을 수 있습니다.

### Dable의 Devops

AWS heavy user인 Dable 개발자로 이번에 해당 서비스를 맡으면서, 다룰 수 있는 서버의 종류도 다양하고 서버 개수도 워낙 많았기에 다양한 실험을 해보며 최적의 운영방안을 고민해볼 수 있었고 실제로 구현까지 해볼 기회가 주어져 큰 배움을 얻을 수 있었습니다. 현재 Dable 개발팀은 EB 사용이 익숙해졌음에도 멈추지 않고 더 효율적인 서버 운영을 위해 쿠버네티스를 적극적으로 도입 중입니다. 쿠버네티스를 이용한 새로운 서버 인스턴스 관리 아키텍처를 다룰 Dable의 다음 포스팅을 기대하며 글을 마치겠습니다. 
