-- Supabase Schema for RTS Game Designer
-- Run this in Supabase Dashboard → SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Kingdoms table
CREATE TABLE IF NOT EXISTS kingdoms (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT DEFAULT '',
    color TEXT DEFAULT '#6ea8fe',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insert default kingdoms
INSERT INTO kingdoms (name, description) VALUES
    ('Humans', 'The baseline kingdom, versatile and balanced'),
    ('Kingdom of Ores', 'Mountain-dwelling master craftsmen and heavy infantry (Dwarves)'),
    ('Kingdom of Magic', 'Arcane-focused faction: Elves, Wizards, Gnomes'),
    ('Kingdom of Evil', 'Dark magic: Necromancers, Witches, Goblins'),
    ('Kingdom of the Ancients', 'Primitive but powerful: Silurian and dinosaurs'),
    ('Kingdom of the Beasts', 'Monstrous creatures: Minotaurs, Trolls, Balrogs, Dragons'),
    ('Kingdom of the Divines', 'Divine beings: Gods, Angels, Demigods, Oracles, Archangels')
ON CONFLICT (name) DO NOTHING;

-- Ages table
CREATE TABLE IF NOT EXISTS ages (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    order_index INTEGER DEFAULT 0,
    color TEXT DEFAULT '#8B7355',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO ages (name, order_index) VALUES
    ('Classical Age', 0),
    ('Medieval Age', 1),
    ('Mythic Age', 2)
ON CONFLICT (name) DO NOTHING;

-- Heroes table
CREATE TABLE IF NOT EXISTS heroes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    hero_name TEXT NOT NULL DEFAULT 'New Hero',
    kingdom TEXT NOT NULL REFERENCES kingdoms(name) ON UPDATE CASCADE,
    age TEXT NOT NULL REFERENCES ages(name) ON UPDATE CASCADE,
    portrait TEXT DEFAULT '',
    extra_images JSONB DEFAULT '[]'::jsonb,
    data JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Schema fields table
CREATE TABLE IF NOT EXISTS fields (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT DEFAULT 'Custom',
    field_type TEXT DEFAULT 'text',
    UNIQUE(name)
);

-- Categories table
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

INSERT INTO categories (name) VALUES
    ('Identity'),
    ('Combat Stats'),
    ('Defense'),
    ('Target Types'),
    ('Range & AoE'),
    ('Abilities'),
    ('Resource'),
    ('Economy'),
    ('Notes'),
    ('Custom')
ON CONFLICT (name) DO NOTHING;

-- Roles table
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Gods table
CREATE TABLE IF NOT EXISTS gods (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Enable Row Level Security (optional - for future auth)
ALTER TABLE heroes ENABLE ROW LEVEL SECURITY;
ALTER TABLE kingdoms ENABLE ROW LEVEL SECURITY;
ALTER TABLE ages ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations (open access for now)
CREATE POLICY "Allow all" ON heroes FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all" ON kingdoms FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow all" ON ages FOR ALL USING (true) WITH CHECK (true);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_heroes_kingdom ON heroes(kingdom);
CREATE INDEX IF NOT EXISTS idx_heroes_age ON heroes(age);
CREATE INDEX IF NOT EXISTS idx_heroes_kingdom_age ON heroes(kingdom, age);
