const version = '0.0.3';
const build_css = require('./build_css');
const build_js = require('./build_js');
const fs = require('fs');
const load_packages = require('./load_packages');
const tar = require('tar-fs');
const zlib = require("zlib");

const distDir = 'dist';
let packageDir = `/ui/pkg/web`;
const destDir = `${distDir}${packageDir}`;
// const args = process.argv.slice(2);
const themes = ['gray', 'noc'];
const queue = [
    ...load_packages('../../../requirements/web.json'),
    ...load_packages('../../../requirements/theme-noc.json')
];

const themeTemplate = '{% if setup.theme == "{theme}" %}\n' +
    `<link rel="stylesheet" type="text/css" href="${packageDir}/app.{app_hash}.{theme}.min.css " />\n` +
    `<script type="text/javascript" src="${packageDir}/vendor.{vendor_hash}.{theme}.min.js"></script>\n` +
    '{% endif %}';

const bundleTemplate = `<script type="text/javascript" src="${packageDir}/boot.{hash}.min.js"></script>\n` +
    '<!-- Include the translations -->\n' +
    `<script type="text/javascript" src="/ui/web/locale/{{ language }}/ext-locale-{{ language }}.js"></script>\n` +
    `<script type="text/javascript" src="${packageDir}/app.{hash}.min.js"></script>\n`;

fs.mkdirSync(destDir, {recursive: true});
fs.mkdirSync(`${destDir}.debug`, {recursive: true});

// ToDo test theme-noc, perhaps need other resources!
function assets(dest, theme) {
    const assetDirs = [
        '.pkg_cache/ui/pkg/fontawesome/fonts'
    ];
    return assetDirs.map(dir =>
        new Promise((resolve, reject) => {
            const name = dir.substr(dir.lastIndexOf('/') + 1);
            tar.pack(dir).pipe(
                tar.extract(`${dest}/${name}`, {
                    finish: () => resolve({name: name, hash: null})
                })
            );
        })
    );
}

function writeBundle(name, data) {
    const dest = `${distDir}/templates`;
    fs.mkdirSync(dest, {recursive: true});
    fs.writeFileSync(`${dest}/${name}.html`, data);
}

function hash(values, file, theme) {
    for(let i = 0; i < values.length; i++) {
        if(values[i].name === file && values[i].theme === theme) {
            return values[i].hash;
        }
    }
    return null;
}

Promise.all(queue).then(values => {
        let stages = [
            // ...assets(destDir, themes),
            ...build_css(destDir, themes),
            ...build_js.application('app', destDir, themes),
            ...build_js.vendor('vendor', destDir, themes),
            ...build_js.boot('boot', destDir, themes),
        ];
        Promise.all(stages).then(values => {
                const output = fs.createWriteStream(`ui-web.tgz`);
                // let content = fs.readFileSync('src/desktop.html').toString();
                let content = bundleTemplate;
                let themeSpecific = [];
                // make desktop.html add hash
                values.filter(value => value.hash | value.theme === '')
                .forEach(value => {
                    const file = value.name.replace(/{hash}/, value.hash);
                    content = content.replace(value.name, file);
                });
                writeBundle('bundle', content);
                // add hash to theme specific files
                themes.forEach(theme => {
                    const appHash = hash(values,'app.{hash}', theme);
                    const vendorHash = hash(values, 'vendor.{hash}', theme);
                    let body;
                    body = themeTemplate.replace(/{theme}/g, theme);
                    body = body.replace(/{app_hash}/, appHash);
                    themeSpecific.push(body.replace(/{vendor_hash}/, vendorHash));
                });
                // content = content.replace(/{theme_specific}/, themeSpecific.join('\n'));
                writeBundle('theme', themeSpecific.join('\n'));
                tar.pack(distDir).pipe(zlib.createGzip()).pipe(output);
                console.log('Done');
            },
            error => {
                console.error(error);
            }
        ).catch(console.error);
    },
    error => {
        console.error(error);
    }
);
