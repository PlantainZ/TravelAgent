-- 用户表 users
CREATE TABLE users (
    id            BIGSERIAL    PRIMARY KEY,
    account       VARCHAR(64)  NOT NULL UNIQUE,          -- 登录账号
    username      VARCHAR(100) NOT NULL,                 -- 显示昵称
    password_hash VARCHAR(255) NOT NULL,                 -- 存哈希，不存明文
    signature     TEXT         DEFAULT '',                -- 个性签名
    avatar_url    TEXT,                                   -- 头像（预留）
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE  users IS '用户主表';
COMMENT ON COLUMN users.password_hash IS '使用 bcrypt/argon2 加密存储';


-- 档案表 archives
CREATE TABLE archives (
    id          BIGSERIAL    PRIMARY KEY,
    title       VARCHAR(255) NOT NULL,                   -- 行程标题，如"2026 国庆·京都五日"
    description TEXT,                                     -- 行程简介
    cover_url   TEXT,                                     -- 封面图（预留）
    status      SMALLINT     NOT NULL DEFAULT 0,          -- 0=策划中 1=进行中 2=已结束 3=已取消
    start_date  DATE,
    end_date    DATE,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_archives_status ON archives (status);
CREATE INDEX idx_archives_date_range ON archives (start_date, end_date);


-- 档案成员关联表 archive_members
CREATE TABLE archive_members (
    id         BIGSERIAL    PRIMARY KEY,
    archive_id BIGINT       NOT NULL REFERENCES archives(id) ON DELETE CASCADE,
    user_id    BIGINT       NOT NULL REFERENCES users(id)    ON DELETE CASCADE,
    role       VARCHAR(20)  NOT NULL,  -- 'creator' | 'planner' | 'viewer'
    joined_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_archive_user UNIQUE (archive_id, user_id),
    CONSTRAINT chk_member_role CHECK (role IN ('creator','planner','viewer'))
);

CREATE INDEX idx_am_user_id  ON archive_members (user_id);
CREATE INDEX idx_am_archive  ON archive_members (archive_id);


-- 票务表 tickets
CREATE EXTENSION postgis;
CREATE TABLE tickets (
    id             BIGSERIAL    PRIMARY KEY,
    archive_id     BIGINT       NOT NULL REFERENCES archives(id) ON DELETE CASCADE,
    name           VARCHAR(255) NOT NULL,                -- 景点/活动名称
    location       VARCHAR(500),                         -- 地点文字描述
    location_point GEOGRAPHY(POINT, 4326),               -- 经纬度（PostGIS）
    booking_app    VARCHAR(255),                         -- 预约 APP / 途径
    target_desc    TEXT,                                  -- 目标（如"抢到2张成人票"）
    booking_time   TIMESTAMPTZ,                          -- 开抢时间
    notes          TEXT,                                  -- 注意事项
    supplement     TEXT,                                  -- 补充/通告内容
    sort_order     INT          NOT NULL DEFAULT 0,       -- 排序
    status         SMALLINT     NOT NULL DEFAULT 0,       -- 0=待抢 1=已抢到 2=失败 3=已取消
    created_at     TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at     TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tickets_archive ON tickets (archive_id);
CREATE INDEX idx_tickets_booking_time ON tickets (booking_time)
    WHERE status = 0;  -- 部分索引：只索引待抢的票，用于提醒/定时任务


-- 前置准备物品表 preparation_items
CREATE TABLE preparation_items (
    id           BIGSERIAL    PRIMARY KEY,
    archive_id   BIGINT       NOT NULL REFERENCES archives(id) ON DELETE CASCADE,
    category     VARCHAR(30)  NOT NULL,  -- 'food' | 'medicine' | 'daily' | 'taboo'(封神榜)
    item_name    VARCHAR(255) NOT NULL,  -- 物品名
    quantity     INT          DEFAULT 1, -- 数量
    note         TEXT,                   -- 备注
    is_checked   BOOLEAN      NOT NULL DEFAULT FALSE,  -- 是否已准备
    assigned_to  BIGINT       REFERENCES users(id),    -- 分配给谁带
    sort_order   INT          NOT NULL DEFAULT 0,      -- 顺序
    created_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_prep_category CHECK (category IN ('food','medicine','daily','taboo'))
);

CREATE INDEX idx_prep_archive ON preparation_items (archive_id);
CREATE INDEX idx_prep_category ON preparation_items (archive_id, category);


-- 行程卡片表 itinerary_cards
CREATE TABLE itinerary_cards (
    id              BIGSERIAL       PRIMARY KEY,
    archive_id      BIGINT          NOT NULL REFERENCES archives(id) ON DELETE CASCADE,
    day_number      INT             NOT NULL DEFAULT 1,   -- 第几天
    spot_name       VARCHAR(255)    NOT NULL,              -- 景点名称
    spot_point      GEOGRAPHY(POINT, 4326),               -- 经纬度
    spot_address    VARCHAR(500),                          -- 文字地址
    visit_duration  INT,                                   -- 预计游览分钟数
    open_time       VARCHAR(100),                          -- 开放时间文字，如"09:00-17:00"
    open_days       VARCHAR(200),                          -- 开放日，如"周二至周日"
    ticket_price    NUMERIC(10,2),                         -- 门票价格（预留）
    notes           TEXT,
    extra           JSONB         DEFAULT '{}',            -- 灵活扩展字段
    sort_order      INT           NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_cards_archive ON itinerary_cards (archive_id);
CREATE INDEX idx_cards_day     ON itinerary_cards (archive_id, day_number, sort_order);
CREATE INDEX idx_cards_extra   ON itinerary_cards USING GIN (extra);


-- 附近吃喝表 nearby_restaurants
CREATE TABLE nearby_restaurants (
    id              BIGSERIAL       PRIMARY KEY,
    card_id         BIGINT          NOT NULL REFERENCES itinerary_cards(id) ON DELETE CASCADE,
    category        VARCHAR(50),     -- 类别：中餐/西餐/咖啡/小吃...
    shop_name       VARCHAR(255)    NOT NULL,
    shop_point      GEOGRAPHY(POINT, 4326),
    shop_address    VARCHAR(500),
    recommended     TEXT[],          -- 推荐菜式数组，如 '{"松鼠桂鱼","响油鳝糊"}'
    phone           VARCHAR(30),
    supports_delivery BOOLEAN       DEFAULT FALSE,
    price_range     VARCHAR(20),     -- 如 "¥50-100/人"
    extra           JSONB           DEFAULT '{}',
    sort_order      INT             NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_rest_card ON nearby_restaurants (card_id);


-- 盖章攻略表 stamp_guides
CREATE TABLE stamp_guides (
    id              BIGSERIAL       PRIMARY KEY,
    card_id         BIGINT          NOT NULL REFERENCES itinerary_cards(id) ON DELETE CASCADE,
    shop_name       VARCHAR(255)    NOT NULL,              -- 盖章店铺
    shop_point      GEOGRAPHY(POINT, 4326),
    shop_address    VARCHAR(500),
    is_free         BOOLEAN         NOT NULL DEFAULT TRUE,
    open_time       VARCHAR(100),
    obtain_method   TEXT,                                   -- 获取方式描述
    stamp_image_url TEXT,                                   -- 章样图片（预留）
    sort_order      INT             NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_stamp_card ON stamp_guides (card_id);


-- 问答-问题表 qa_questions
CREATE TABLE qa_questions (
    id          BIGSERIAL    PRIMARY KEY,
    archive_id  BIGINT       NOT NULL REFERENCES archives(id) ON DELETE CASCADE,
    asker_id    BIGINT       NOT NULL REFERENCES users(id),
    title       VARCHAR(500) NOT NULL,
    content     TEXT,
    is_resolved BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_qa_archive ON qa_questions (archive_id);
CREATE INDEX idx_qa_asker   ON qa_questions (asker_id);


-- 问答-回答表 qa_answers
CREATE TABLE qa_answers (
    id           BIGSERIAL    PRIMARY KEY,
    question_id  BIGINT       NOT NULL REFERENCES qa_questions(id) ON DELETE CASCADE,
    answerer_id  BIGINT       NOT NULL REFERENCES users(id),
    content      TEXT         NOT NULL,
    is_accepted  BOOLEAN      NOT NULL DEFAULT FALSE,      -- 是否被采纳
    created_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ans_question ON qa_answers (question_id);
CREATE INDEX idx_ans_answerer ON qa_answers (answerer_id);


-- 自动维护 updated_at 的通用触发器函数
CREATE OR REPLACE FUNCTION fn_update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 为所有有 updated_at 的表绑定触发器
DO $$
DECLARE
    tbl TEXT;
BEGIN
    FOR tbl IN
        SELECT unnest(ARRAY[
            'users','archives','tickets','itinerary_cards',
            'nearby_restaurants','stamp_guides','qa_questions','qa_answers'
        ])
    LOOP
        EXECUTE format(
            'CREATE TRIGGER trg_%s_updated
             BEFORE UPDATE ON %I
             FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp()',
            tbl, tbl
        );
    END LOOP;
END $$;


