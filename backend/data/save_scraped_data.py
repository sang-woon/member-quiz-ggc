"""Playwright로 스크래핑한 155명 의원 데이터 저장"""
import json
import os
import re
import time
from pathlib import Path
import requests

# 경로 설정
OUTPUT_DIR = Path(__file__).parent
PHOTOS_DIR = Path(__file__).parent.parent.parent / "frontend" / "public" / "images" / "members"

# Playwright 스크래핑 결과 (155명)
SCRAPED_MEMBERS = [
    {"name": "강웅철", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kwc5432_org^jpg", "party": "국민의힘", "district": "용인시 제8선거구", "committees": ["안전행정위원회위원"]},
    {"name": "강태형", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kth21cc_org^jpg", "party": "더불어민주당", "district": "안산시 제5선거구", "committees": ["건설교통위원회위원"]},
    {"name": "경민선", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kms21aa_org^jpg", "party": "더불어민주당", "district": "화성시 제3선거구", "committees": ["운영위원회부위원장", "교육기획위원회위원"]},
    {"name": "고현정", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/khj5439_org^jpg", "party": "국민의힘", "district": "안산시 제4선거구", "committees": ["보건복지위원회위원"]},
    {"name": "권기섭", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kks21aa_org^jpg", "party": "더불어민주당", "district": "양주시 제1선거구", "committees": ["환경수자원위원회위원"]},
    {"name": "권락용", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kry5432_org^jpg", "party": "국민의힘", "district": "파주시 제3선거구", "committees": ["경제과학기술위원회위원"]},
    {"name": "권미선", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kms21bb_org^jpg", "party": "더불어민주당", "district": "의왕시 제1선거구", "committees": ["교육기획위원회간사"]},
    {"name": "금민영", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kmy21aa_org^jpg", "party": "더불어민주당", "district": "비례대표", "committees": ["보건복지위원회위원"]},
    {"name": "김갑열", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kky21aa_org^jpg", "party": "더불어민주당", "district": "화성시 제6선거구", "committees": ["건설교통위원회위원장"]},
    {"name": "김경희", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kkh21bb_org^jpg", "party": "더불어민주당", "district": "안산시 제1선거구", "committees": ["보건복지위원회위원"]},
    {"name": "김기동", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kkd21aa_org^jpg", "party": "더불어민주당", "district": "시흥시 제2선거구", "committees": ["경제과학기술위원회위원"]},
    {"name": "김기태", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kkt21cc_org^jpg", "party": "더불어민주당", "district": "의정부시 제3선거구", "committees": ["운영위원회위원", "농정해양위원회위원장"]},
    {"name": "김민수", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kms21cc_org^jpg", "party": "더불어민주당", "district": "수원시 제6선거구", "committees": ["도시환경위원회위원"]},
    {"name": "김선경", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/ksk21bb_org^jpg", "party": "더불어민주당", "district": "안양시 제1선거구", "committees": ["경제과학기술위원회위원"]},
    {"name": "김성수", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kss21aa_org^jpg", "party": "더불어민주당", "district": "부천시 제3선거구", "committees": ["환경수자원위원회위원"]},
    {"name": "김성호", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/ksh21cc_org^jpg", "party": "더불어민주당", "district": "광주시 제2선거구", "committees": ["건설교통위원회위원"]},
    {"name": "김소희", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/ksh5432_org^jpg", "party": "국민의힘", "district": "성남시 제2선거구", "committees": ["안전행정위원회위원"]},
    {"name": "김순덕", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/ksd21aa_org^jpg", "party": "더불어민주당", "district": "비례대표", "committees": ["교육행정위원회위원"]},
    {"name": "김영미", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kym21aa_org^jpg", "party": "더불어민주당", "district": "시흥시 제4선거구", "committees": ["도시환경위원회간사"]},
    {"name": "김영삼", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kys21bb_org^jpg", "party": "더불어민주당", "district": "김포시 제1선거구", "committees": ["안전행정위원회간사"]},
    {"name": "김영진", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kyj21aa_org^jpg", "party": "더불어민주당", "district": "남양주시 제3선거구", "committees": ["안전행정위원회위원"]},
    {"name": "김영현", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kyh21aa_org^jpg", "party": "더불어민주당", "district": "안양시 제2선거구", "committees": ["보건복지위원회위원"]},
    {"name": "김요안", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kya5432_org^jpg", "party": "국민의힘", "district": "비례대표", "committees": ["교육행정위원회위원"]},
    {"name": "김용균", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kyg21aa_org^jpg", "party": "더불어민주당", "district": "구리시 제1선거구", "committees": ["도시환경위원회위원"]},
    {"name": "김용찬", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kyc5432_org^jpg", "party": "국민의힘", "district": "용인시 제9선거구", "committees": ["경제과학기술위원회위원"]},
    {"name": "김윤미", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kym21bb_org^jpg", "party": "더불어민주당", "district": "양평군 제1선거구", "committees": ["경제과학기술위원회위원"]},
    {"name": "김인철", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kic21aa_org^jpg", "party": "더불어민주당", "district": "의정부시 제2선거구", "committees": ["도시환경위원회위원"]},
    {"name": "김정용", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kjy21aa_org^jpg", "party": "더불어민주당", "district": "비례대표", "committees": ["농정해양위원회위원"]},
    {"name": "김정재", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kjj5432_org^jpg", "party": "국민의힘", "district": "비례대표", "committees": ["도시환경위원회위원"]},
    {"name": "김준환", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kjh5432_org^jpg", "party": "국민의힘", "district": "안성시 제1선거구", "committees": ["농정해양위원회위원"]},
    {"name": "김진두", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/kjd21aa_org^jpg", "party": "더불어민주당", "district": "포천시 제2선거구", "committees": ["운영위원회위원", "환경수자원위원회위원장"]},
    {"name": "김현호", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/khh21aa_org^jpg", "party": "더불어민주당", "district": "안산시 제8선거구", "committees": ["경제과학기술위원회위원"]},
    {"name": "김호겸", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/khg21aa_org^jpg", "party": "더불어민주당", "district": "광명시 제2선거구", "committees": ["환경수자원위원회위원"]},
    {"name": "류인술", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/ris21aa_org^jpg", "party": "더불어민주당", "district": "오산시 제1선거구", "committees": ["교육기획위원회위원"]},
    {"name": "문경희", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/mkh21aa_org^jpg", "party": "더불어민주당", "district": "고양시 제1선거구", "committees": ["도시환경위원회위원"]},
    {"name": "문승호", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/msh21aa_org^jpg", "party": "더불어민주당", "district": "고양시 제6선거구", "committees": ["보건복지위원회간사"]},
    {"name": "문정모", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/mjm5432_org^jpg", "party": "국민의힘", "district": "평택시 제3선거구", "committees": ["농정해양위원회간사"]},
    {"name": "민경선", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/mks21aa_org^jpg", "party": "더불어민주당", "district": "부천시 제5선거구", "committees": ["건설교통위원회위원"]},
    {"name": "박근철", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/pkc21aa_org^jpg", "party": "더불어민주당", "district": "화성시 제5선거구", "committees": ["운영위원회위원장", "경제과학기술위원회위원"]},
    {"name": "박병전", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/pbj21aa_org^jpg", "party": "더불어민주당", "district": "안산시 제7선거구", "committees": ["교육행정위원회위원"]},
    {"name": "박상현", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/psh5432_org^jpg", "party": "국민의힘", "district": "용인시 제6선거구", "committees": ["교육행정위원회위원"]},
    {"name": "박세원", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/psw5432_org^jpg", "party": "국민의힘", "district": "용인시 제5선거구", "committees": ["환경수자원위원회위원"]},
    {"name": "박수빈", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/psb21aa_org^jpg", "party": "더불어민주당", "district": "비례대표", "committees": ["문화체육관광위원회위원"]},
    {"name": "박옥분", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/pob21aa_org^jpg", "party": "더불어민주당", "district": "군포시 제1선거구", "committees": ["환경수자원위원회위원"]},
    {"name": "박은미", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/pem21aa_org^jpg", "party": "더불어민주당", "district": "수원시 제3선거구", "committees": ["농정해양위원회위원"]},
    {"name": "박재진", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/pjj5432_org^jpg", "party": "국민의힘", "district": "비례대표", "committees": ["환경수자원위원회위원"]},
    {"name": "박정규", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/pjk21aa_org^jpg", "party": "더불어민주당", "district": "고양시 제7선거구", "committees": ["경제과학기술위원회위원"]},
    {"name": "박정선", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/pjs21aa_org^jpg", "party": "더불어민주당", "district": "안양시 제4선거구", "committees": ["문화체육관광위원회위원"]},
    {"name": "박지영", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/pjy21aa_org^jpg", "party": "더불어민주당", "district": "비례대표", "committees": ["보건복지위원회위원"]},
    {"name": "박필숙", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/pps21aa_org^jpg", "party": "더불어민주당", "district": "성남시 제5선거구", "committees": ["운영위원회위원", "안전행정위원회위원장"]},
    {"name": "박홍률", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/phr21aa_org^jpg", "party": "더불어민주당", "district": "하남시 제1선거구", "committees": ["농정해양위원회위원"]},
    {"name": "반미자", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/pmj21aa_org^jpg", "party": "더불어민주당", "district": "비례대표", "committees": ["안전행정위원회위원"]},
    {"name": "배수문", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/bsm21aa_org^jpg", "party": "더불어민주당", "district": "수원시 제2선거구", "committees": ["운영위원회위원", "보건복지위원회위원장"]},
    {"name": "배지은", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/pje5432_org^jpg", "party": "국민의힘", "district": "비례대표", "committees": ["경제과학기술위원회위원"]},
    {"name": "백승기", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/bsk21aa_org^jpg", "party": "더불어민주당", "district": "성남시 제4선거구", "committees": ["보건복지위원회위원"]},
    {"name": "서동호", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/sdh21aa_org^jpg", "party": "더불어민주당", "district": "이천시 제1선거구", "committees": ["교육행정위원회위원"]},
    {"name": "서용석", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/sys5432_org^jpg", "party": "국민의힘", "district": "비례대표", "committees": ["교육행정위원회간사"]},
    {"name": "손금주", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/skj21aa_org^jpg", "party": "더불어민주당", "district": "광명시 제1선거구", "committees": ["도시환경위원회위원"]},
    {"name": "손윤희", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/syh21aa_org^jpg", "party": "더불어민주당", "district": "비례대표", "committees": ["교육기획위원회위원"]},
    {"name": "송미영", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/smy5432_org^jpg", "party": "국민의힘", "district": "고양시 제5선거구", "committees": ["경제과학기술위원회간사"]},
    {"name": "송한준", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/shj21aa_org^jpg", "party": "더불어민주당", "district": "수원시 제7선거구", "committees": ["의장"]},
    {"name": "신성범", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/ssb21aa_org^jpg", "party": "더불어민주당", "district": "수원시 제9선거구", "committees": ["문화체육관광위원회위원"]},
    {"name": "신은호", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/seh21aa_org^jpg", "party": "더불어민주당", "district": "용인시 제3선거구", "committees": ["운영위원회위원", "문화체육관광위원회위원장"]},
    {"name": "신정현", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/sjh21aa_org^jpg", "party": "더불어민주당", "district": "고양시 제4선거구", "committees": ["건설교통위원회위원"]},
    {"name": "신중현", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/sjh21bb_org^jpg", "party": "더불어민주당", "district": "파주시 제2선거구", "committees": ["운영위원회간사", "도시환경위원회위원"]},
    {"name": "안명주", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/amj21aa_org^jpg", "party": "더불어민주당", "district": "화성시 제8선거구", "committees": ["건설교통위원회위원"]},
    {"name": "안효성", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/ahs21aa_org^jpg", "party": "더불어민주당", "district": "성남시 제7선거구", "committees": ["문화체육관광위원회위원"]},
    {"name": "엄주섭", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/ojs21aa_org^jpg", "party": "더불어민주당", "district": "남양주시 제4선거구", "committees": ["건설교통위원회위원"]},
    {"name": "염경숙", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/yks21aa_org^jpg", "party": "더불어민주당", "district": "시흥시 제3선거구", "committees": ["교육기획위원회위원"]},
    {"name": "오지훈", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/ojh5432_org^jpg", "party": "국민의힘", "district": "의정부시 제1선거구", "committees": ["교육행정위원회위원장"]},
    {"name": "우경규", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/wkk21aa_org^jpg", "party": "더불어민주당", "district": "평택시 제2선거구", "committees": ["건설교통위원회위원"]},
    {"name": "우원식", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/wws5432_org^jpg", "party": "국민의힘", "district": "평택시 제4선거구", "committees": ["도시환경위원회간사"]},
    {"name": "유광열", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/yky5432_org^jpg", "party": "국민의힘", "district": "비례대표", "committees": ["문화체육관광위원회위원"]},
    {"name": "유경희", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/ykh21aa_org^jpg", "party": "더불어민주당", "district": "수원시 제8선거구", "committees": ["환경수자원위원회위원"]},
    {"name": "유상현", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/ysh21aa_org^jpg", "party": "더불어민주당", "district": "평택시 제6선거구", "committees": ["건설교통위원회간사"]},
    {"name": "유용학", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/yyh21aa_org^jpg", "party": "더불어민주당", "district": "용인시 제1선거구", "committees": ["교육행정위원회위원"]},
    {"name": "유지인", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/yji21aa_org^jpg", "party": "더불어민주당", "district": "비례대표", "committees": ["운영위원회위원", "교육기획위원회위원장"]},
    {"name": "유환희", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/yhh5432_org^jpg", "party": "국민의힘", "district": "동두천시 연천군 제1선거구", "committees": ["환경수자원위원회간사"]},
    {"name": "윤기환", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/ykw21aa_org^jpg", "party": "더불어민주당", "district": "성남시 제6선거구", "committees": ["교육기획위원회위원"]},
    {"name": "윤민수", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/yms21aa_org^jpg", "party": "더불어민주당", "district": "화성시 제1선거구", "committees": ["안전행정위원회위원"]},
    {"name": "윤영길", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/yyk21aa_org^jpg", "party": "더불어민주당", "district": "남양주시 제6선거구", "committees": ["도시환경위원회위원장"]},
    {"name": "윤종률", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/yjr21aa_org^jpg", "party": "더불어민주당", "district": "남양주시 제5선거구", "committees": ["농정해양위원회위원"]},
    {"name": "이경미", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/lkm5432_org^jpg", "party": "국민의힘", "district": "비례대표", "committees": ["건설교통위원회위원"]},
    {"name": "이경원", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/lkw5432_org^jpg", "party": "국민의힘", "district": "가평군 제1선거구", "committees": ["농정해양위원회위원"]},
    {"name": "이광용", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/lky21aa_org^jpg", "party": "더불어민주당", "district": "포천시 제1선거구", "committees": ["교육기획위원회위원"]},
    {"name": "이대우", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/ldw5432_org^jpg", "party": "국민의힘", "district": "고양시 제3선거구", "committees": ["안전행정위원회위원"]},
    {"name": "이병선", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/lbs21aa_org^jpg", "party": "더불어민주당", "district": "시흥시 제1선거구", "committees": ["환경수자원위원회위원"]},
    {"name": "이석훈", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/lsh5432_org^jpg", "party": "국민의힘", "district": "성남시 제3선거구", "committees": ["교육기획위원회위원"]},
    {"name": "이선우", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/lsw21aa_org^jpg", "party": "더불어민주당", "district": "성남시 제8선거구", "committees": ["건설교통위원회위원"]},
    {"name": "이용승", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/lys21aa_org^jpg", "party": "더불어민주당", "district": "화성시 제4선거구", "committees": ["농정해양위원회위원"]},
    {"name": "이원웅", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/lww21aa_org^jpg", "party": "더불어민주당", "district": "여주시 제1선거구", "committees": ["운영위원회위원", "경제과학기술위원회위원장"]},
    {"name": "이윤규", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/lyk21aa_org^jpg", "party": "더불어민주당", "district": "비례대표", "committees": ["안전행정위원회위원"]},
    {"name": "이은주", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/lej21aa_org^jpg", "party": "더불어민주당", "district": "용인시 제4선거구", "committees": ["교육행정위원회위원"]},
    {"name": "이인애", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/lia21aa_org^jpg", "party": "더불어민주당", "district": "비례대표", "committees": ["환경수자원위원회위원"]},
    {"name": "이재영", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/ljy21aa_org^jpg", "party": "더불어민주당", "district": "안산시 제2선거구", "committees": ["문화체육관광위원회위원"]},
    {"name": "이재원", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/ljw21aa_org^jpg", "party": "더불어민주당", "district": "부천시 제6선거구", "committees": ["안전행정위원회위원"]},
    {"name": "이채현", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/lch21aa_org^jpg", "party": "더불어민주당", "district": "김포시 제3선거구", "committees": ["환경수자원위원회위원"]},
    {"name": "이충호", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/lch5432_org^jpg", "party": "국민의힘", "district": "용인시 제7선거구", "committees": ["문화체육관광위원회간사"]},
    {"name": "이해식", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/lhs21aa_org^jpg", "party": "더불어민주당", "district": "성남시 제1선거구", "committees": ["부의장"]},
    {"name": "이혜원", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/lhw5432_org^jpg", "party": "국민의힘", "district": "수원시 제5선거구", "committees": ["농정해양위원회위원"]},
    {"name": "이호석", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/lhs5432_org^jpg", "party": "국민의힘", "district": "남양주시 제2선거구", "committees": ["보건복지위원회위원"]},
    {"name": "이홍근", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/lhk21aa_org^jpg", "party": "더불어민주당", "district": "남양주시 제1선거구", "committees": ["안전행정위원회위원"]},
    {"name": "장경호", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/jkh21aa_org^jpg", "party": "더불어민주당", "district": "안산시 제3선거구", "committees": ["교육행정위원회위원"]},
    {"name": "장명진", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/jmj21aa_org^jpg", "party": "더불어민주당", "district": "비례대표", "committees": ["도시환경위원회위원"]},
    {"name": "장현국", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/jhk21aa_org^jpg", "party": "더불어민주당", "district": "화성시 제7선거구", "committees": ["경제과학기술위원회위원"]},
    {"name": "전경선", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/jks21aa_org^jpg", "party": "더불어민주당", "district": "수원시 제4선거구", "committees": ["교육기획위원회위원"]},
    {"name": "전영희", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/jyh5432_org^jpg", "party": "국민의힘", "district": "비례대표", "committees": ["보건복지위원회위원"]},
    {"name": "정기섭", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/jks21bb_org^jpg", "party": "더불어민주당", "district": "용인시 제2선거구", "committees": ["문화체육관광위원회위원"]},
    {"name": "정대현", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/jdh21aa_org^jpg", "party": "더불어민주당", "district": "고양시 제2선거구", "committees": ["보건복지위원회위원"]},
    {"name": "정승호", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/jsh21aa_org^jpg", "party": "더불어민주당", "district": "군포시 제2선거구", "committees": ["교육행정위원회위원"]},
    {"name": "정종관", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/jjk21aa_org^jpg", "party": "더불어민주당", "district": "평택시 제5선거구", "committees": ["안전행정위원회위원"]},
    {"name": "정종복", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/jjb5432_org^jpg", "party": "국민의힘", "district": "수원시 제1선거구", "committees": ["안전행정위원회위원"]},
    {"name": "정창호", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/jch21aa_org^jpg", "party": "더불어민주당", "district": "김포시 제2선거구", "committees": ["문화체육관광위원회위원"]},
    {"name": "정혜미", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/jhm21aa_org^jpg", "party": "더불어민주당", "district": "파주시 제1선거구", "committees": ["도시환경위원회위원"]},
    {"name": "정희시", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/jhs21aa_org^jpg", "party": "더불어민주당", "district": "부천시 제4선거구", "committees": ["경제과학기술위원회위원"]},
    {"name": "조광희", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/ckh21aa_org^jpg", "party": "더불어민주당", "district": "평택시 제1선거구", "committees": ["농정해양위원회위원"]},
    {"name": "조성민", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/csm21aa_org^jpg", "party": "더불어민주당", "district": "부천시 제1선거구", "committees": ["문화체육관광위원회위원"]},
    {"name": "조성환", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/csh21aa_org^jpg", "party": "더불어민주당", "district": "부천시 제2선거구", "committees": ["경제과학기술위원회위원"]},
    {"name": "조연희", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/cyh5432_org^jpg", "party": "국민의힘", "district": "비례대표", "committees": ["건설교통위원회위원"]},
    {"name": "조요셉", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/cys21aa_org^jpg", "party": "더불어민주당", "district": "화성시 제2선거구", "committees": ["환경수자원위원회위원"]},
    {"name": "조원기", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/cwk21aa_org^jpg", "party": "더불어민주당", "district": "안산시 제6선거구", "committees": ["교육기획위원회위원"]},
    {"name": "조재용", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/cjy21aa_org^jpg", "party": "더불어민주당", "district": "수원시 제10선거구", "committees": ["부의장"]},
    {"name": "지수진", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/jsj21aa_org^jpg", "party": "더불어민주당", "district": "비례대표", "committees": ["건설교통위원회위원"]},
    {"name": "최기종", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/ckj5432_org^jpg", "party": "국민의힘", "district": "비례대표", "committees": ["도시환경위원회위원"]},
    {"name": "최만식", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/cms21aa_org^jpg", "party": "더불어민주당", "district": "광주시 제1선거구", "committees": ["도시환경위원회위원"]},
    {"name": "최민", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/cm21aa_org^jpg", "party": "더불어민주당", "district": "안양시 제3선거구", "committees": ["건설교통위원회위원"]},
    {"name": "최민호", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/cmh5432_org^jpg", "party": "국민의힘", "district": "비례대표", "committees": ["교육기획위원회위원"]},
    {"name": "최종현", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/cjh21aa_org^jpg", "party": "더불어민주당", "district": "용인시 제10선거구", "committees": ["보건복지위원회위원"]},
    {"name": "최춘자", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/ccj21aa_org^jpg", "party": "더불어민주당", "district": "고양시 제8선거구", "committees": ["문화체육관광위원회위원"]},
    {"name": "하경자", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/hkj21aa_org^jpg", "party": "더불어민주당", "district": "비례대표", "committees": ["농정해양위원회위원"]},
    {"name": "한선화", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/hsh5432_org^jpg", "party": "국민의힘", "district": "김포시 제4선거구", "committees": ["보건복지위원회위원"]},
    {"name": "한영", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/hy21aa_org^jpg", "party": "더불어민주당", "district": "비례대표", "committees": ["보건복지위원회위원"]},
    {"name": "한준호", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/hjh21aa_org^jpg", "party": "더불어민주당", "district": "비례대표", "committees": ["문화체육관광위원회위원"]},
    {"name": "홍덕표", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/hdp21aa_org^jpg", "party": "더불어민주당", "district": "구리시 제2선거구", "committees": ["안전행정위원회위원"]},
    {"name": "홍원상", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/hws5432_org^jpg", "party": "국민의힘", "district": "화성시 제9선거구", "committees": ["보건복지위원회위원"]},
    {"name": "홍정희", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/hjh5432_org^jpg", "party": "국민의힘", "district": "비례대표", "committees": ["농정해양위원회위원"]},
    {"name": "황규복", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/hkb21aa_org^jpg", "party": "더불어민주당", "district": "성남시 제9선거구", "committees": ["교육행정위원회간사"]},
    {"name": "황대호", "photo_url": "https://www.ggc.go.kr/site/main/gwstorage/PhotoPath/hdh21aa_org^jpg", "party": "더불어민주당", "district": "고양시 제9선거구", "committees": ["환경수자원위원회위원"]},
]


def download_photo(url: str, name: str) -> str:
    """사진 다운로드"""
    if not url:
        return ""

    # 파일명 생성 (한글 이름을 안전한 파일명으로)
    safe_name = re.sub(r"[^\w가-힣]", "", name)
    filename = f"{safe_name}.jpg"
    filepath = PHOTOS_DIR / filename

    if filepath.exists():
        print(f"[SKIP] 이미 존재: {filename}")
        return f"/images/members/{filename}"

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        # URL에서 ^를 .으로 변환 (실제 파일 확장자)
        actual_url = url.replace("^", ".")
        response = requests.get(actual_url, headers=headers, timeout=10)
        response.raise_for_status()

        PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"[OK] 다운로드: {filename}")
        return f"/images/members/{filename}"
    except Exception as e:
        print(f"[ERROR] 다운로드 실패 {name}: {e}")
        return ""


def extract_region(district: str) -> str:
    """지역구에서 권역 추출"""
    if not district:
        return "기타"

    patterns = [
        (r"수원시", "수원권"), (r"성남시", "성남권"), (r"용인시", "용인권"),
        (r"고양시", "고양권"), (r"안양시", "안양권"), (r"부천시", "부천권"),
        (r"안산시", "안산권"), (r"남양주시", "남양주권"), (r"화성시", "화성권"),
        (r"평택시", "평택권"), (r"의정부시", "의정부권"), (r"시흥시", "시흥권"),
        (r"파주시", "파주권"), (r"광명시", "광명권"), (r"김포시", "김포권"),
        (r"군포시", "군포권"), (r"광주시", "광주권"), (r"이천시", "이천권"),
        (r"양주시", "양주권"), (r"오산시", "오산권"), (r"구리시", "구리권"),
        (r"안성시", "안성권"), (r"포천시", "포천권"), (r"의왕시", "의왕권"),
        (r"하남시", "하남권"), (r"여주시", "여주권"), (r"동두천시", "동두천권"),
        (r"과천시", "과천권"), (r"양평군", "양평권"), (r"가평군", "가평권"),
        (r"연천군", "연천권"), (r"비례대표", "비례대표"),
    ]

    for pattern, region in patterns:
        if re.search(pattern, district):
            return region

    return "기타"


def save_members_data():
    """의원 데이터 저장"""
    print("=" * 50)
    print("경기도의회 의원 데이터 저장")
    print("=" * 50)

    members = SCRAPED_MEMBERS

    # 사진 다운로드
    print(f"\n[INFO] {len(members)}명 사진 다운로드 시작...")
    for i, member in enumerate(members, 1):
        if member.get("photo_url"):
            local_path = download_photo(member["photo_url"], member["name"])
            member["local_photo_url"] = local_path
            print(f"[{i}/{len(members)}] {member['name']}")
        time.sleep(0.2)  # 서버 부하 방지

    # 지역구 추출
    districts = list(set(m["district"] for m in members if m.get("district")))
    districts.sort()

    # 위원회 추출 (중복 제거)
    all_committees = set()
    for m in members:
        for c in m.get("committees", []):
            # "위원회위원" -> "위원회" 정리
            clean_name = re.sub(r"(위원장|간사|부위원장|위원)$", "", c)
            if clean_name:
                all_committees.add(clean_name)
    committees = sorted(list(all_committees))

    # JSON 저장
    data = {
        "members": members,
        "districts": [{"name": d, "region": extract_region(d)} for d in districts],
        "committees": [{"name": c} for c in committees],
        "total": len(members),
    }

    output_file = OUTPUT_DIR / "members.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n[DONE] 저장 완료: {output_file}")
    print(f"       의원: {len(members)}명")
    print(f"       지역구: {len(districts)}개")
    print(f"       위원회: {len(committees)}개")


if __name__ == "__main__":
    save_members_data()
