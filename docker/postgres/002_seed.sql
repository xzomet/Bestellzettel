-- Tables
INSERT INTO tables (name, is_active)
VALUES
  ('Table 1', true),
  ('Table 2', true),
  ('Table 3', true),
  ('Table 4', true)
ON CONFLICT DO NOTHING;

-- VORSPEISEN / APPETIZERS
INSERT INTO menu_items (category, name, price_cents, is_active)
VALUES
  ('vorspeisen', 'Austern', 450, true),
  ('vorspeisen', 'Scharfe Paste', 990, true),
  ('vorspeisen', 'Hummus', 990, true),
  ('vorspeisen', 'Cacik', 990, true),
  ('vorspeisen', 'Avocadocreme', 990, true),
  ('vorspeisen', 'Auberginen Joghurt', 990, true),
  ('vorspeisen', 'Kalter Oktopus', 1790, true),

-- SUPPEN / SOUPS
  ('suppen', 'Fischsuppe', 850, true),

-- SALATE / SALADS
  ('salad', 'Thunfischsalat', 1950, true),
  ('salad', 'Atlantik Fisch Salat', 1850, true),
  ('salad', 'Lachssalat', 1950, true),
  ('salad', 'Garnelensalat', 1990, true),

-- FISCH BAGUETTES
  ('baguette', 'Sardellen Baguette', 1100, true),
  ('baguette', 'Lachs Baguette', 1250, true),
  ('baguette', 'Doradenfilet Baguette', 1250, true),

-- MEERESFRÜCHTE / SEAFOOD MAIN DISHES
  ('haupt', 'Sardellen', 1990, true),
  ('haupt', 'Gemischte Platte', 2890, true),
  ('haupt', 'Rote Meerbarben', 2490, true),
  ('haupt', 'K. Rote Meerbarben', 2490, true),
  ('haupt', 'Merlan', 1990, true),
  ('haupt', 'Blaufisch', 2490, true),
  ('haupt', 'Dorade', 2700, true),
  ('haupt', 'Wolfsbarsch', 2700, true),
  ('haupt', 'Forelle', 2390, true),
  ('haupt', 'Makrele', 2490, true),
  ('haupt', 'Scholle', 2250, true),
  ('haupt', 'Stöcker', 1990, true),
  ('haupt', 'Seezunge', 3500, true),
  ('haupt', 'Lachskotelett', 2200, true),
  ('haupt', 'Pangasiusfilet', 1990, true),
  ('haupt', 'Rotbarschfilet', 2490, true),
  ('haupt', 'Viktoriabarschfilet', 2390, true),
  ('haupt', 'Steinbeisserfilet', 2490, true),
  ('haupt', 'Seelachsfilet', 1990, true),
  ('haupt', 'Kabeljaufilet', 2490, true),
  ('haupt', 'Thunfisch', 2790, true),

-- BEILAGEN / SIDE DISHES
  ('beilagen', 'Reis', 750, true),
  ('beilagen', 'Pommes frites', 490, true),
  ('beilagen', 'Salzkartoffeln', 490, true),
  ('beilagen', 'Kartoffelecken', 490, true),
  ('beilagen', 'Knoblauchbrot', 550, true),
  ('beilagen', 'Joghurt Peperoni', 900, true),

-- GETRÄNKE / DRINKS
  ('drinks', 'Bier', 490, true),
  ('drinks', 'Cola', 290, true),
  ('drinks', 'Wein', 750, true),
  ('drinks', 'Raki', 750, true),

-- DESSERTS / DESERTS
  ('deserts', 'Künefe', 750, true),
  ('deserts', 'Baklava', 600, true)
ON CONFLICT DO NOTHING;
