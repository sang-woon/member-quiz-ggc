-- Supabase PostgreSQL 스키마
-- Supabase SQL Editor에서 실행하세요

-- 지역구 테이블
CREATE TABLE IF NOT EXISTS districts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    region VARCHAR(50)
);

-- 위원회 테이블
CREATE TABLE IF NOT EXISTS committees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- 의원 테이블
CREATE TABLE IF NOT EXISTS members (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    photo_url VARCHAR(500) NOT NULL,
    party VARCHAR(50),
    district_id INTEGER NOT NULL REFERENCES districts(id),
    term INTEGER DEFAULT 11
);

-- 의원-위원회 연결 테이블
CREATE TABLE IF NOT EXISTS member_committees (
    id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
    committee_id INTEGER NOT NULL REFERENCES committees(id) ON DELETE CASCADE,
    UNIQUE(member_id, committee_id)
);

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_members_district_id ON members(district_id);
CREATE INDEX IF NOT EXISTS idx_members_party ON members(party);
CREATE INDEX IF NOT EXISTS idx_member_committees_member_id ON member_committees(member_id);
CREATE INDEX IF NOT EXISTS idx_member_committees_committee_id ON member_committees(committee_id);

-- Row Level Security (선택사항 - 공개 읽기 허용)
ALTER TABLE districts ENABLE ROW LEVEL SECURITY;
ALTER TABLE committees ENABLE ROW LEVEL SECURITY;
ALTER TABLE members ENABLE ROW LEVEL SECURITY;
ALTER TABLE member_committees ENABLE ROW LEVEL SECURITY;

-- 모든 사용자에게 읽기 권한 부여
CREATE POLICY "Allow public read access on districts" ON districts FOR SELECT USING (true);
CREATE POLICY "Allow public read access on committees" ON committees FOR SELECT USING (true);
CREATE POLICY "Allow public read access on members" ON members FOR SELECT USING (true);
CREATE POLICY "Allow public read access on member_committees" ON member_committees FOR SELECT USING (true);
