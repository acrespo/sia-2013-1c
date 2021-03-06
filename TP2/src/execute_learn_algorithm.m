function data = execute_learn_algorithm(W, matrix_topology, g, gp, window_size, params)


  load('TimeSerie_G1.mat');
  x = (x + 4) ./ 8;
  dataset = zeros(window_size, 800);
  for i=1:800
    dataset(:,i) = x(i:i+window_size-1)';
  end
  expected = x(window_size+1:800+window_size);

  test_set = zeros(window_size, 200-window_size);
  for i=801:1000-window_size
    test_set(:,i-800) = x(i:i+window_size-1)';
  end
  test_results = x(801+window_size:1000);

	data = learn(dataset, expected, W, g, gp, params);

  testset_output = zeros(size(test_results));

  err = []
  for i=1:size(test_set, 2)
     y = run_neural_network(W, test_set(:,i), g);
     y = y.V.(char('@'+(size(fieldnames(y.V), 1))));
     testset_output(i) = y;
     err = [err norm(y - test_results(i))];
   end
   data.testset_output = testset_output;
   disp(mean(err));

end
