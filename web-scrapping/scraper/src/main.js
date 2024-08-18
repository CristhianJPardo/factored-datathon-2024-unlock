import { CheerioCrawler } from 'crawlee';
import { URL } from 'node:url';
import fs from 'fs';
import path from 'path';
//const data = fs.readFileSync('source_urls.json', 'utf8');
//const urls_list = JSON.parse(data);

function sanitizeTitle(title) {
    return title.replace(/[\/\\?%*:|"<>]/g, '_').trim() + '.json';
}

const crawler = new CheerioCrawler({
    maxRequestsPerCrawl: 20,
    async requestHandler({ request, $ }) {
        //const title = $('title').text();
        //console.log(`The title of "${request.url}" is: ${title}.`);
        // Obtén el título de la página
        const title = $('title').text();
        // Extrae el contenido de todos los elementos <p>
        const paragraphs = $('p').map((i, el) => $(el).text()).get();
        
        // Crea un objeto con el título y los párrafos
        const data = {
            title: title,
            content: paragraphs
        };
        const fileName = sanitizeTitle(title);
        const directory = 'extraction';
        const filePath = path.join(directory, fileName);
        
        // Asegúrate de que la carpeta exista
        if (!fs.existsSync(directory)) {
            fs.mkdirSync(directory, { recursive: true });
        }

        // Guarda el objeto en un archivo JSON
        fs.writeFileSync(filepath, JSON.stringify(data, null, 2), 'utf-8');
        
        console.log('Datos guardados en output.json');

        const links = $('a[href]')
            .map((_, el) => $(el).attr('href'))
            .get();

        // Besides resolving the URLs, we now also need to
        // grab their hostname for filtering.
        const { hostname } = new URL(request.loadedUrl);
        const absoluteUrls = links.map((link) => new URL(link, request.loadedUrl));

        // We use the hostname to filter links that point
        // to a different domain, even subdomain.
        const sameHostnameLinks = absoluteUrls
            .filter((url) => url.hostname === hostname)
            .map((url) => ({ url: url.href }));

        // Finally, we have to add the URLs to the queue
        await crawler.addRequests(sameHostnameLinks);
    },
});

// await crawler.run([...urls_list])
await crawler.run(["https://www.eldoradonews.com/news/2023/aug/13/sanders-picks-new-secretary-of-state-parks/"])
