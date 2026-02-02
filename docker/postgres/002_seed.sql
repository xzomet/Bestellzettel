-- Tables
INSERT INTO tables (name, is_active)
VALUES
  ('Table 1', true),
  ('Table 2', true),
  ('Table 3', true),
  ('Table 4', true)
ON CONFLICT DO NOTHING;

-- VORSPEISEN / APPETIZERS
INSERT INTO menu_items (name, price_cents, is_active)
VALUES
  ('Austern', 450, true),
  ('Scharfe Paste', 990, true),
  ('Hummus', 990, true),
  ('Cacik', 990, true),
  ('Avocadocreme', 990, true),
  ('Auberginen Joghurt', 990, true),
  ('Kalter Oktopus', 1790, true),

-- SUPPEN / SOUPS
  ('Fischsuppe', 850, true),

-- SALATE / SALADS
  ('Thunfischsalat', 1950, true),
  ('Atlantik Fisch Salat', 1850, true),
  ('Lachssalat', 1950, true),
  ('Garnelensalat', 1990, true),

-- FISCH BAGUETTES
  ('Sardellen Baguette', 1100, true),
  ('Lachs Baguette', 1250, true),
  ('Doradenfilet Baguette', 1250, true),

-- MEERESFRÜCHTE / SEAFOOD MAIN DISHES
  ('Sardellen', 1990, true),
  ('Gemischte Platte', 2890, true),
  ('Rote Meerbarben', 2490, true),
  ('K. Rote Meerbarben', 2490, true),
  ('Merlan', 1990, true),
  ('Blaufisch', 2490, true),
  ('Dorade', 2700, true),
  ('Wolfsbarsch', 2700, true),
  ('Forelle', 2390, true),
  ('Makrele', 2490, true),
  ('Scholle', 2250, true),
  ('Stöcker', 1990, true),
  ('Seezunge', 3500, true),
  ('Lachskotelett', 2200, true),
  ('Pangasiusfilet', 1990, true),
  ('Rotbarschfilet', 2490, true),
  ('Viktoriabarschfilet', 2390, true),
  ('Steinbeisserfilet', 2490, true),
  ('Seelachsfilet', 1990, true),
  ('Kabeljaufilet', 2490, true),
  ('Thunfisch', 2790, true),

-- BEILAGEN / SIDE DISHES
  ('Reis', 750, true),
  ('Pommes frites', 490, true),
  ('Salzkartoffeln', 490, true),
  ('Kartoffelecken', 490, true),
  ('Knoblauchbrot', 550, true),
  ('Joghurt Peperoni', 900, true),

-- GETRÄNKE / DRINKS
  ('Bier', 490, true),
  ('Cola', 290, true),
  ('Wein', 750, true),
  ('Raki', 750, true)
ON CONFLICT DO NOTHING;
