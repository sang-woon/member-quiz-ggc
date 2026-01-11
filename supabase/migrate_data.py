"""SQLite 데이터를 Supabase SQL INSERT 문으로 변환"""
import json
import os
import re


def escape_sql(value):
    """SQL 문자열 이스케이프"""
    if value is None:
        return "NULL"
    if isinstance(value, str):
        return "'" + value.replace("'", "''") + "'"
    return str(value)


def generate_insert_sql():
    """INSERT SQL 생성"""
    # members.json 파일 읽기
    data_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'data', 'members.json')

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    districts = data['districts']
    committees = data['committees']
    members = data['members']

    sql_lines = []
    sql_lines.append("-- 자동 생성된 데이터 INSERT 문")
    sql_lines.append("-- Supabase SQL Editor에서 schema.sql 실행 후 이 파일을 실행하세요\n")

    # 지역구 INSERT (ID 매핑 생성)
    sql_lines.append("-- 지역구 데이터")
    district_name_to_id = {}
    for i, d in enumerate(districts, 1):
        district_name_to_id[d['name']] = i
        sql_lines.append(
            f"INSERT INTO districts (id, name, region) VALUES ({i}, {escape_sql(d['name'])}, {escape_sql(d.get('region'))});"
        )
    sql_lines.append("")

    # 위원회 INSERT (ID 매핑 생성)
    sql_lines.append("-- 위원회 데이터")
    committee_name_to_id = {}
    for i, c in enumerate(committees, 1):
        committee_name_to_id[c['name']] = i
        sql_lines.append(
            f"INSERT INTO committees (id, name) VALUES ({i}, {escape_sql(c['name'])});"
        )
    sql_lines.append("")

    # 의원 INSERT
    sql_lines.append("-- 의원 데이터")
    for i, m in enumerate(members, 1):
        district_name = m.get('district', '')
        district_id = district_name_to_id.get(district_name, 1)  # 기본값 1
        photo_url = m.get('local_photo_url', '') or m.get('photo_url', '')

        sql_lines.append(
            f"INSERT INTO members (id, name, photo_url, party, district_id, term) VALUES "
            f"({i}, {escape_sql(m['name'])}, {escape_sql(photo_url)}, "
            f"{escape_sql(m.get('party'))}, {district_id}, 11);"
        )
    sql_lines.append("")

    # 의원-위원회 연결 INSERT
    sql_lines.append("-- 의원-위원회 연결 데이터")
    mc_id = 1
    for i, m in enumerate(members, 1):
        member_id = i
        for committee_str in m.get('committees', []):
            # 위원회명에서 역할 제거 (위원장, 부위원장, 간사, 위원)
            clean_name = re.sub(r'(위원장|부위원장|간사|위원)$', '', committee_str)
            committee_id = committee_name_to_id.get(clean_name)

            if committee_id:
                sql_lines.append(
                    f"INSERT INTO member_committees (id, member_id, committee_id) VALUES ({mc_id}, {member_id}, {committee_id});"
                )
                mc_id += 1
    sql_lines.append("")

    # 시퀀스 리셋
    sql_lines.append("-- 시퀀스 리셋 (PostgreSQL)")
    sql_lines.append(f"SELECT setval('districts_id_seq', {len(districts)});")
    sql_lines.append(f"SELECT setval('committees_id_seq', {len(committees)});")
    sql_lines.append(f"SELECT setval('members_id_seq', {len(members)});")
    sql_lines.append(f"SELECT setval('member_committees_id_seq', {mc_id - 1});")

    return "\n".join(sql_lines)


if __name__ == "__main__":
    sql = generate_insert_sql()

    # SQL 파일로 저장
    output_path = os.path.join(os.path.dirname(__file__), 'data.sql')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(sql)

    print(f"데이터 SQL 생성 완료: {output_path}")
    print(f"Supabase SQL Editor에서 다음 순서로 실행하세요:")
    print(f"  1. supabase/schema.sql")
    print(f"  2. supabase/data.sql")
