/*global window, angular, console*/
(function (angular) {
  'use strict';

  angular.module('numeter', ['ui.bootstrap']).
    directive('graph', ['$http', function ($http) {
      return {
        scope: {
          resolution: '=',
          url: '=',
        },
        templateUrl: 'media/graph.html',
        link: function ($scope, $element) {
          numeter.get_graph($scope.url, $element[0], $scope.resolution);
        },
        controller: ['$scope', '$http', function ($scope, $http) {
          console.log($scope.url);
        }]
      };
    }]).
    directive('menu', ['$http', function ($http) {
      return {
        templateUrl: 'media/menu.html',
        link: function ($scope) {
          $http.get('rest/hosts/').
            success(function (data) {
              $scope.hosts = data.results;
            });
        },
        controller: ['$scope', '$http', function ($scope, $http) {
          $scope.loadCategories = function (hosts) {
            angular.forEach(hosts, function (host) {
              $http.get('hosttree/host/' + host.id).
                success(function (categories) {
                  host.categories = categories.map(function (category) {
                    return {name: category, plugins: [], open: false};
                  });
                });
            });
          };

          $scope.loadPlugins = function (host, chosen_category) {
            angular.forEach(host.categories, function (category) {
                  if ( chosen_category == category ) {
              $http.get('hosttree/category/' + host.id, {params: {category: category.name}}).
                success(function (plugins) {
                  category.plugins = plugins;
                    $scope.displayGraph(host.id, plugins, true);
                });
                  }
            });
          };

          $scope.displayGraph = function (host_id, plugins, open) {
            if (open) {
              return;
            }
            $scope.$emit('displayGraph', host_id, plugins);
          };

        }]
      };
    }]).
    controller('resolutionCtrl', ['$scope', function ($scope) {
      $scope.select = function (value) {
        $scope.$emit('resChange', value);
      };
    }]).
    controller('graphCtrl', ['$scope', function ($scope) {
      $scope.selected = 'Daily';
      $scope.$on('resChange', function (event, resolution) {
        $scope.selected = resolution;
      });

      $scope.$on('displayGraph', function (event, host_id, plugins) {
        $scope.graphs = [];
        plugins.map(function (plugin) {          
          this.push({url: "get/graph/" + host_id + "/" + plugin.plugin, resolution: $scope.selected });
        }, $scope.graphs);
      });
      $scope.$on('resChange', function (event) {
        var old_graphs = $scope.graphs;
        $scope.graphs = []
        old_graphs.map(function (graph) {          
          this.push({url: graph.url, resolution: $scope.selected });
        }, $scope.graphs);
      });
    }]);

}(angular));
