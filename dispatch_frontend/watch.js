var gulp = require('gulp');
var exec = require('child_process').exec;

gulp.task('typescript change',
    (callback) => {
         var buildAction = new Promise(
            (resolve, reject) => {
                    exec('npm run build',

                        (error) => {
                            if (error)
                                {
                                    console.log(error);
                                    resolve();
                                    return callback(error);
                                }
                            callback();
                            resolve();
                        }
                 );
            }
         );
         buildAction.then(
            () => {
                console.log('done.');
            }
         );
    }
);

var watcher = gulp.watch('src/**/*', ['typescript change']);
watcher.on('change',
    () => {
        console.log('changes to src code detected, running build and deploy tasks...');
    }
);