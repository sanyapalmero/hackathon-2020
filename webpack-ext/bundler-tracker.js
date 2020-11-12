// The MIT License (MIT)

// Copyright (c) 2015 Owais Lone

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

var path = require('path');
var fs = require('fs');
var stripAnsi = require('strip-ansi');
var mkdirp = require('mkdirp');
var extend = require('deep-extend');

var assets = {};
var DEFAULT_OUTPUT_FILENAME = 'webpack-stats.json';
var DEFAULT_LOG_TIME = false;


function Plugin(options) {
  this.contents = {};
  this.options = options || {};
  this.options.filename = this.options.filename || DEFAULT_OUTPUT_FILENAME;
  if (this.options.logTime === undefined) {
    this.options.logTime = DEFAULT_LOG_TIME;
  }
}

Plugin.prototype.apply = function(compiler) {
    var self = this;

    const _compilation = function(compilation, callback) {
      const failedModule = function(fail){
        var output = {
          status: 'error',
          error: fail.error.name || 'unknown-error'
        };
        if (fail.error.module !== undefined) {
          output.file = fail.error.module.userRequest;
        }
        if (fail.error.error !== undefined) {
          output.message = stripAnsi(fail.error.error.codeFrame);
        } else {
          output.message = '';
        }
        self.writeOutput(compiler, output);
      };

      if (compilation.hooks){
        const plugin = {name: 'BundleTrackerPlugin'};
        compilation.hooks.failedModule.tap(plugin, failedModule);
      } else {
        compilation.plugin('failed-module', failedModule);
      }
    };

    const compile = function(factory, callback) {
      self.writeOutput(compiler, {status: 'compiling'});
    };

    const done = function(stats) {
      if (stats.compilation.errors.length > 0) {
        var error = stats.compilation.errors[0];
        self.writeOutput(compiler, {
          status: 'error',
          error: error['name'] || 'unknown-error',
          message: stripAnsi(error['message'])
        });
        return;
      }

      // Files loaded with file-loader are not being output to
      // stats.compilation.chunks[#].files. We build chunks map
      // by inspecting the output folder directly.
      // It is assumed that files named in the format [chunkName]-[hash].[ext]
      var fsChunkMap = {};
      fs.readdirSync(compiler.options.output.path).forEach(function(file){
        var chunk = file.split('-').slice(0, -1).join('-');
        if (!fsChunkMap[chunk]) fsChunkMap[chunk] = [];
        fsChunkMap[chunk].push(file);
      });
      var fsChunks = []
      for (var chunk in fsChunkMap) {
        if (!fsChunkMap.hasOwnProperty(chunk)) continue;
        fsChunks.push({
          name: chunk,
          files: fsChunkMap[chunk],
        });
      }

      var chunks = {};
      fsChunks.map(function(chunk){
        var files = chunk.files.map(function(file){
          var F = {name: file};
          var publicPath = self.options.publicPath || compiler.options.output.publicPath;
          if (publicPath) {
            F.publicPath = publicPath + file;
          }
          if (compiler.options.output.path) {
            F.path = path.join(compiler.options.output.path, file);
          }
          return F;
        });
        chunks[chunk.name] = files;
      });
      var output = {
        status: 'done',
        chunks: chunks
      };

      if (self.options.logTime === true) {
        output.startTime = stats.startTime;
        output.endTime = stats.endTime;
      }

      self.writeOutput(compiler, output);
    };

    if (compiler.hooks) {
      const plugin = {name: 'BundleTrackerPlugin'};
      compiler.hooks.compilation.tap(plugin, _compilation);
      compiler.hooks.compile.tap(plugin, compile);
      compiler.hooks.done.tap(plugin, done);
    } else {
      compiler.plugin('compilation', compilation);
      compiler.plugin('compile', compile);
      compiler.plugin('done', done);
    }
};


Plugin.prototype.writeOutput = function(compiler, contents) {
    var outputDir = this.options.path || '.';
    var outputFilename = path.join(outputDir, this.options.filename || DEFAULT_OUTPUT_FILENAME);
    var publicPath = this.options.publicPath || compiler.options.output.publicPath;
    if (publicPath) {
        contents.publicPath = publicPath;
    }
    mkdirp.sync(path.dirname(outputFilename));

    this.contents = extend(this.contents, contents);
    fs.writeFileSync(
        outputFilename,
        JSON.stringify(this.contents, null, this.options.indent)
    );
};

module.exports = Plugin;
