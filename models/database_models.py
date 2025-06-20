TRANSLATION_RECORDS_TABLE = '''
CREATE TABLE IF NOT EXISTS translation_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_text TEXT NOT NULL,
    translated_text TEXT,
    source_lang TEXT,
    target_lang TEXT,
    file_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hash TEXT
);
'''

USER_CONFIG_TABLE = '''
CREATE TABLE IF NOT EXISTS user_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    api_key TEXT,
    base_url TEXT,
    default_source_lang TEXT,
    default_target_lang TEXT,
    concurrency INTEGER,
    cache_policy TEXT
);
'''

CACHE_STATS_TABLE = '''
CREATE TABLE IF NOT EXISTS cache_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hash TEXT,
    hit_count INTEGER DEFAULT 0,
    last_hit TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''
