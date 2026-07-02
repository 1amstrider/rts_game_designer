-- Supabase Schema for RTS Game Designer
-- Run this in Supabase Dashboard → SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Kingdoms table (with rich profiles)
CREATE TABLE IF NOT EXISTS kingdoms (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT DEFAULT '',
    forefathers TEXT DEFAULT '',
    established TEXT DEFAULT '',
    races TEXT DEFAULT '',
    history TEXT DEFAULT '',
    color TEXT DEFAULT '#6ea8fe',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insert default kingdoms with rich bios
INSERT INTO kingdoms (name, description, forefathers, established, races, history) VALUES
    ('Humans', 'Versatile and balanced. Masters of adaptation and technology.', 'The First Men', 'Classical Age', 'Humans', 'The First Men built the earliest civilizations. Over ages they mastered warfare, diplomacy, and technology. Though individually weaker than other races, their unity and innovation allowed them to thrive. They established the first codes of law and the concept of standing armies.'),
    ('Kingdom of Ores', 'Mountain-dwelling master craftsmen and heavy infantry.', 'Durin the Deathless', 'Classical Age', 'Dwarves', 'Forged in the heart of mountains, the dwarves were created by the god Moradin from stone and fire. Durin the Deathless was the first of their kind. They built labyrinthine halls beneath peaks, mastered metallurgy and rune-magic. Their grudges last generations, but their loyalty is absolute.'),
    ('Kingdom of Magic', 'Arcane-focused faction wielding powerful spellcraft.', 'Archmage Aelindor', 'Medieval Age', 'Elves, Wizards, Gnomes', 'When the veil between worlds thinned, the Elves emerged from the Feywilds. Aelindor, the first Archmage, taught mortals to harness mana. Later, the Gnomes brought alchemical ingenuity. Together they built the Crystal Spires, academies of magic that float above forests. Their power peaks in the Mythic Age.'),
    ('Kingdom of Evil', 'Practitioners of dark magic, necromancy, and forbidden arts.', 'Lich Lord Vorthak', 'Medieval Age', 'Necromancers, Witches, Goblins', 'Vorthak was once a noble wizard who sought immortality. His experiments with death magic corrupted him and his followers. From his Black Citadel, he raised the first undead legions. Witches and goblins flocked to his banner, drawn by promises of power. They thrive on decay, corruption, and the forbidden.'),
    ('Kingdom of the Ancients', 'Primitive but powerful beings bonded with primordial beasts.', 'Great Mother Sauria', 'Classical Age', 'Silurian, Dinosaurs', 'Before the rise of civilization, the Silurian people roamed jungles alongside dinosaurs. Great Mother Sauria was the first to bond with a T-Rex through blood rituals. They reject magic and technology, relying on primal strength and beast companions. Their empire once covered half the world.'),
    ('Kingdom of the Beasts', 'Monstrous creatures of immense physical power.', 'Baal the Horned King', 'Classical Age', 'Minotaurs, Trolls, Balrogs, Dragons, Serpents', 'Baal was the first Minotaur to unite the monster tribes beneath the volcanic peaks of Ashmoor. Trolls, Balrogs, and Dragons pledged fealty to his strength. They value dominance above all. Their arenas run with blood, and only the strong survive.'),
    ('Kingdom of the Divines', 'Divine beings of holy power and celestial might.', 'The Creator Athenia', 'Classical Age', 'Gods, Angels, Demigods, Oracles, Archangels', 'Athenia, the Creator, breathed life into the first angels from starlight. They built the Celestial Citadel above the clouds. Demigods are the offspring of gods and mortals. Oracles see all possible futures. The Divines represent absolute order, purity, and judgment against the forces of darkness.')
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
