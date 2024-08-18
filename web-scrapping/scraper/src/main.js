import { CheerioCrawler } from 'crawlee';
import { URL } from 'node:url';
import fs from 'fs';
import path from 'path';

function sanitizeTitle(title) {
    return title.replace(/[\/\\?%*:|"<>]/g, '_').trim() + '.json';
}

const crawler = new CheerioCrawler({
    maxRequestsPerCrawl: 1, // Limita el número de solicitudes por crawl a 1
    async requestHandler({ request, $ }) {
        const title = $('title').text();
        const paragraphs = $('p').map((i, el) => $(el).text()).get();
        
        const data = {
            title: title,
            content: paragraphs
        };
        const fileName = sanitizeTitle(title);
        const directory = 'extraction';
        const filePath = path.join(directory, fileName);
        
        if (!fs.existsSync(directory)) {
            fs.mkdirSync(directory, { recursive: true });
        }

        fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf-8');
        
        console.log(`Datos guardados en ${filePath}`);

        // No agregar enlaces a la cola para evitar el crawling de otras páginas
    },
});

await crawler.run(["https://www.eldoradonews.com/news/2023/aug/13/sanders-picks-new-secretary-of-state-parks/"]);

