function run_tests()

  replace_algorithms = [...
    @replace_1, @replace_2, @replace_3...
  ];

  replace_algorithms_names = [...
    'replace_1', 'replace_2', 'replace_3'...
  ];

  needs_G = [false true true];
  
  N_range = [5 20 80 160];
  
  G_range = [0.6 0.9];
  
  selection_algorithms = [...
    @elite, ...
    @rank, ...
    @(x, y, z)(tournament(x, y, 0.75)), ...
    @roulette, ...
    @(x, y, z)(boltzmann(x, y, z.g)), ...
    @(x, y, z)(boltzmann(x, y, 0.5*z.g)), ...
    @(x, y, z)(mix1(x, y, 0.3*y)), ...
    @(x, y, z)(mix1(x, y, 0.7*y)), ...
    @(x, y, z)(mix2(x, y, 0.3*y)), ...
    @(x, y, z)(mix2(x, y, 0.7*y)) ...
  ];

  selection_algorithms_names = [...
    'elite', ...
    'rank', ...
    'roulette', ...
    'tournament 0.75', ...
    'boltzmann T = 0.5 * generations', ...
    'boltzmann T = generations', ...
    'mix roulette + 30% elite', ...
    'mix roulette + 70% elite', ...
    'mix stochastic + 30% elite', ...
    'mix stochastic + 70% elite' ...
  ];
    
  mutation_algorithms = [ ...
    @(x)(x), ...
    @(x)(single_mutate(x, 0.90, (rand()-0.5))), ...
    @(x)(universal_mutate(x, 0.95, 0.5)), ...
    @(x)(universal_mutate(x, 0.98, 0.5)) ...
  ];
  
  mutation_algorithms_names = [ ...
    'no mutation', ...
    'single mutation 90% of individuals', ...
    'universal_mutate, 0.95 per allel', ...
    'universal_mutate, 0.98 per allel' ...
  ];

  cross_algorithms = [ ...
    @(x, y)(anular(x, y, 10)), ...
    @(x, y)(anular(x, y, 30)), ...
    @(x, y)(uniform_cross(x, y, 0.6)), ...
    @crossover, ...
    @double_crossover ...
  ];
    
  cross_algorithms_names = [...
    'anular, L = 10', ...
    'anular, L = 30', ...
    'universal_cross 0.6', ...
    'crossover', ...
    'double_crossover' ...
  ];