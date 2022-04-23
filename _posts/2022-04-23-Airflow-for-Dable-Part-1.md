---
layout: post
title: 'Airflow for Dable Part 1 - Dable Airflow System Structure'
date: 2022-04-23 00:00:00 +0900
author: Hanul Lee
tags: [data pipeline, workflow orchestration, data engineering, devops, airflow, kubernetes]
---

안녕하세요! 데이블 Data Platform (DP) 팀입니다.

지금까지 블로그에서 DP라는 팀을 본 적이 없어 생소하게 느끼실텐데, DP 팀은 데이블의 Data를 안정적으로 제공하기 위해 2021년부터 AI팀으로부터
분리된 신생 팀으로 고객 데이터부터 회사 내에서 활용하는 비즈니스 데이터까지 회사에서 필요한 데이터를 제공하는 시스템을 만드는 팀입니다.

DP 팀이 신설된 이후 팀에서는 이전 Data Pipeline 시스템을 점검하고 보다 더 안정적인 시스템으로 만들기 위한 일을 주로 해왔습니다. 회사가
점점 성장하고 있는 단계에서 현재의 시스템으로는 비즈니스 요구 사항을 만족시키기 힘든 부분이 있었고, 따라서 저희는 새로운 Workflow Platform을
도입하여 Data Pipeline을 구성하고 기존의 코드들을 이전하기로 결정하였습니다.

DP 팀은 2021년 2월부터 Data Pipeline 시스템 이전을 결정하고 작업을 시작하였는데요, 이번 포스트들을 통해 DP팀이 Data Pipeline 시스템 이전을
결정하였을 때부터 지금까지 어떤 기술적 결정들을 내렸으며 어떤 작업을 진행했는지 이야기해 보고자 합니다.

앞으로 이야기할 주제는 다음과 같습니다.

1. 젖과 꿀이 흐르는 땅, Airflow로!
2. Dable의 Airflow System 구성
3. Airflow에서 DAG 실행을 위한 Convention 정의
4. Airflow 도입 후의 이슈들 (Multi-timezone issue 등)
5. Airflow 도입 후 Dable의 시스템 장애 상황과 운영

# 젖과 꿀이 흐르는 땅, Airflow로!
데이블의 기존 Data Pipeline System은 Jenkins로 구성이 되어 있었습니다. Jenkins는 CI (Continuous Integration)를 위해 만들어진 툴이면서
cron과 각 job들 간의 dependency를 설정할 수 있기 때문에 Jenkins에 job을 추가하여 Data Workflow를 구성할 수 있었습니다.
그러나 언급했듯이 원래 Jenkins는 Data Workflow를 위해서 설계된 툴이 아니다보니 Jenkins를 통해 Data Pipeline System을 운영하는 것은 몇 가지
한계점이 있었습니다.

1. Jenkins에서 간단한 Job Dependency는 설정할 수 있었지만, 복잡한 Dependency는 설정하는 것이 불가능했습니다. 두 개의 Job이 실행되고 나서
실행되어야 하는 Job이 있다고 한다면, 먼저 실행되어야 하는 Job 하나에만 Dependency를 설정할 수 있었으며 다른 하나의 선행 Job은 후행 Job이
실행되기 전에 끝나도록 cron 설정을 해주어야 했습니다. 이러한 상황은 Workflow 설계 이후 어느 정도 시간이 지났을 때 dependency를 추적하고
Job을 관리하는데 문제가 되었고 또한 선행 Job의 시스템 장애 발생 시 데이터 복구에 어려움이 있었습니다.
2. Jenkins에서 Job이 제대로 실행되고 있는지, 얼마나 실패하고 어느 정도 시간이 드는지에 대한 모니터링이 어려웠습니다.
3. Jenkins에서 Job이 실패하면 retry하는 옵션이 존재했지만, 시간별 데이터, 일간 데이터를 구하는 Job들의 경우 실행 시간에 따라 결과가 달라질
수 있기 때문에 사실상 자가 복구는 불가능했습니다. 이로 인해 복구에 리소스를 많이 투자해야 했습니다.
4. 점차 데이터가 커지게 될 경우 Jenkins로는 더이상 scalability를 보장하기 어려웠습니다.

이러한 한계로 인해 Jenkins 사용이 더 이상 힘들 것이라 판단했고, 이러한 한계들을 극복할 수 있는 Workflow Orchestration이 가능한 Platform으로의
이전을 위해 Workflow Platform들에 대한 조사를 진행했습니다.

![Comparision table](/techblog/assets/images/2021-09-30-Airflow-for-Dable-Part-1/1.png) <sup>[[1]](#footnote_1)</sup>

여러 Workflow Platform 중에 저희 팀에서 선택한 것은 Apache Airflow이었습니다. Luigi, Prefect, KubeFlow 등의 다양한 선택지 중에
Airflow를 선택한 이유는 1) 현재 굉장히 많은 회사/팀에서 Airflow를 사용하고 있어 발전이 매우 빠르며 광범위한 생태계가 형성되어 있어 버그
등의 이슈 처리가 빠르고 2) 팀에서 다루는 대다수 데이터 처리 코드가 Python으로 구성되어 있어 Python Open Source Platform인 Airflow의 도입이
쉽고, 3) task 실행헤 있어서 여러 Operator를 선택해 원하는 여러 환경에서 task 실행이 가능하며, Scheduler/Worker 등의 확장성이 높아
안정적이고 확장성 있는 Workflow Orchestration이 가능했기 때문입니다. <sup>[[2]](#footnote_2)</sup>

Airflow로의 이전을 결정하고, 팀에서는 한 달 간의 테스트를 통해서 Airflow를 사용하는 방식과 Airflow 시스템 구성을 위한 감을 잡았습니다.
Airflow에서의 Job 실행은 Jenkins에서의 그것과 많이 달랐기 때문에 DAG (Directed Acyclic Graph) 구현, Airflow config settings
(Scheduler, Webserver), Job Executor, Operator 등에 대한 개념을 잡아갔으며 어떻게 시스템을 구성해야할지 고민하고 결정하였습니다.
오랜 고민과 테스트 끝에 우리는 Airflow가 젖과 꿀이 흐르는 땅이라고 믿으며 Airflow로 Workflow Orchestration System을 구성하기 시작했습니다.

# Dable의 Airflow System 구성
Dable의 Airflow System 구성은 다음과 같습니다.

![Dable Airflow Structure](/techblog/assets/images/2021-09-30-Airflow-for-Dable-Part-1/2.png)

다른 회사에서의 Airflow System 구성들을 살펴보면 Airflow on Kubernetes (Kubernetes 위에 Airflow를 pod으로 띄우고 실행하는 방식)를
선택하는 경우가 많은데, Dable에서는 Airflow Scheduler와 Airflow Webserver를 하나의 서버(EC2 Instance)에서 실행하도록 하였습니다.
이렇게 구성한 것에는 두 가지 이유가 있습니다. 첫째로는 DP 팀에서는 Airflow를 오직 Workflow Orchestration의 용도로만 사용하고 싶었고,
따라서 Workflow 구성과 실제 Workflow의 실행 주체를 분리하고 싶었습니다. 이전 시스템이었던 Jenkins와 마찬가지로 관리와 실행이 하나의
서버에서 이루어진다면, 관리와 복구가 용이한 Airflow로 이전하는 이유가 퇴색될 것으로 여겼습니다. 
두번째로는 Kubernetes에서 Airflow가 실행되는 경우 Kubernetes가 SPOF(단일장애점, single point of failure)되어 Kubernetes에 장애가
생길 시 문제가 될 수도 있다고 판단했습니다. Kubernetes에 여러 pod으로 Airflow Scheduler/Webserver/Worker가 띄어져 있는 상황에서
Kubernetes 내의 특정 노드에 문제가 생긴다면 치명적일 수도 있기 때문입니다.
다만 이러한 방식은 Airflow on Kubernetes에 비해서 Airflow Scheduler의 scale out을 하기 어렵다는 단점이 있습니다. Data Pipeline이
점차 늘어나게 된다면 해당 방식을 좀 더 Scalable한 방식으로 바꿔야 할 필요가 있을텐데, 이를 위해 저희는 미리 전체 시스템을 구성하는 script
를 설계하고 구현해놓아 훗날의 문제를 방지하고자 했습니다.
Airflow Scheduler와 Webserver가 한 개의 서버에서 돌아간다면 실제 DAG 내의 task들은 AWS EKS cluster에서 실행됩니다. 이를 위해서
KubernetesPodOperator를 사용하였고, 지정된 EKS cluster에서 task별로 pod을 실행하도록 구성하였습니다.

task의 실행을 위해 우리는 KubernetesPodOperator를 상속하여 새로운 Custom Operator를 만들었습니다. 구현한 Custom Operator는
팀에서 정한 규칙에 맞춰 task를 Kubernetes에서 실행시키도록 합니다. task를 실행시키는 pod이 차지하는 request/limit resource나, 이전
task의 실패에 따른 시간 종속성이 있는 task들은 이전 task의 복구 전까지 scheduling하지 않게 설정하도록 하는 등의 여러 설정이
해당 Custom Operator에 정의되었습니다.

![Airflow_Custom_Operator]()

전체적인 시스템의 구성도 중요하지만 실제 코드들이 어떻게 지속적으로 배포(CI/CD)되는지도 중요합니다. Kubernetes에서 task를 실행하기 위해
Docker image가 필요한데, 실행할 Docker image는 AWS ECR에서 받아오도록 설정하였습니다. 저희가 사용하는 Airflow 버전(2.0.0)에는
build에 대한 versioning을 따로 관리하는 방법이 없어 Docker image를 실행할 때 특정 tag를 지정하는 방식으로 빌드된 코드들의 version을
관리하도록 하였습니다.
만약 task 실행 시 특정 tag를 받지 않는다면 Airflow variable로 저장되어 있는 최신 tag를 통해 최신의 Docker image를 가져오게 하여
최신 코드를 유지하도록 설계하였습니다.

Docker image 내에는 코드를 실행시키기 위한 Python 2/3 환경과 필요한 라이브러리들, 그리고 실행할 코드가 포함됩니다. 코드는 Dockerfile
build 시 Git에서 pull해오도록 되어있는데, PR이 merge되어 실행할 코드들이 수정되어 배포할 필요가 있다면 정의된 Dockerfile과 script를
통해 Docker image를 빌드하게 되고, 이를 새로운 tag를 붙여 ECR에 배포합니다. 배포 이후 새로운 tag는 위에서 언급한 Airflow variable로
저장됩니다.

실제 task 실행 코드는 Kubernetes pod으로 실행되기 때문에 Docker image를 통해 배포되지만, 저희는 Airflow와 Kubernetes를 분리했기
때문에 DAG 코드의 경우는 Airflow server로 배포되어야 합니다. Airflow DAG 코드의 수정이 있어 배포가 필요하다면, 정의된 script를 통해
직접 Airflow server로 배포합니다. 배포된 version은 시간별로 Airflow server 내에서 관리하고, 최근 배포에 문제가 있다면 server에서 직접
rollback하도록 되어 있습니다.

![Airflow_Customized_Logger](/techblog/assets/images/2021-09-30-Airflow-for-Dable-Part-1/4.png)

Airflow Monitoring은 크게 3가지 관점에서 이루어집니다. 첫번째로는 DAG 관점으로, task 실행 중에 어떤 문제가 생겨 DAG가 실패하는 경우입니다.
이 경우 task fail은 Airflow의 Slack Webhook 기능을 활용하여 Slack notification으로 전송됩니다. 전송된 후에는 Airflow Webserver를
통해 문제가 생긴 DAG의 log를 확인하고, 문제를 파악해 코드를 수정하고 Docker image를 재배포하는 등의 조치를 취합니다.
기존의 Airflow의 경우 server local log를 삭제하지 않기 때문에 Airflow server의 용량이 부족하거나 하는 문제가 생길 수 있는데요, 그래서
저희는 custom logger를 추가 구현하여 local log에는 retention을 부여하도록 하고, AWS S3에도 원격으로 로그가 저장되도록 설정하였습니다.
새로 정의한 custom logger를 airflow.cfg의 logging_config_class에 지정함으로써, custom logger를 사용하여 logging을 하도록
설정할 수 있습니다.

![Airflow_Grafana](/techblog/assets/images/2021-09-30-Airflow-for-Dable-Part-1/5.png)

두번째로는 Airflow Worker 관점의 모니터링입니다. 여기서 Airflow worker는 Kubernetes pod들로 실행이 되기 때문에, Kubernetes의 노드들
의 resource 상황이나 pod 상황을 모니터링할 필요가 있습니다. 팀에서는 Kubernetes를 모니터링하는 방법 중 가장 널리 알려져 있는 Prometheus
& Grafana 조합을 활용하여 node와 pod의 CPU/Memory를 모니터링하도록 구현하였고, 문제가 생길 시 Slack notification을 전송하도록 Alert
Manager를 구성하였습니다.
  
마지막으로는 Airflow Scheduler 관점에서의 모니터링입니다. Scheduler 관점에서는 실행되고 있는 DAG들이 잘 실행되고 있는지, 얼마나 실패했는지,
실행 시간이 얼마나 증가했는지 등에 대한 전체 Pipeline의 상황을 확인할 필요가 있습니다. 이를 위해서는 Airflow가 제공하는 metrics를 활용해야
하는데, Airflow에서는 statsd를 통해 이러한 metrics을 제공하고 있습니다. 따라서 저희는 Airflow statsd와 연결을 위한 statsd-exporter를
Airflow server에 docker container로 구성하였으며, 이를 Prometheus & Grafana와 연동하여 Worker 관점과 동일한 방식으로 모니터링하도록
하였습니다.

# 마치며
이번 포스트를 통해 DP 팀에서 Airflow를 선택한 이유와 Airflow를 통해 어떻게 Data Pipeline System을 구성하였는지에 대해서 공유해보았습니다.
앞으로는 System 구성 이후 DP팀에서 어떤 문제들을 풀어야했는지를 공유할 예정으로, 다음 포스트에는 팀에서 Airflow를 실제로 사용해보면서 당면했던 여러
이슈들과 이러한 이슈들을 해결했던 방법, Airflow 운영을 위해 정한 팀내 Convetion 등을 다뤄 볼 예정입니다.


<a name="footnote_1">[1]</a> https://www.datarevenue.com/en-blog/airflow-vs-luigi-vs-argo-vs-mlflow-vs-kubeflow

<a name="footnote_2">[2]</a> Airflow의 많은 장점에도 불구하고 실제 결정에는 팀의 상황에 따라 Workflow Platform을 신중하게 선택할 필요가
있습니다. 데이블 내에서도 AI 팀은 Machine Learning Experiment를 위해 Prefect로 Workflow Orchestration System을 구성하였는데,
이는 Airflow 2.0.0에서는 Machine Learning Workflow를 구성하는 데에는 몇 가지 한계점이 존재했기 때문입니다.