import "dotenv/config.js"

import { crawler } from './crawler.js'
import { emptyResources, getMultipleUrlsToScrape, getNewsSize, logRunTime, markUrlsAsScraped, newsToS3, saveNewsAsJson } from './helpers.js'

const NUM_REQUESTS_TO_QUEUE = parseInt(process.env.NUM_REQUESTS_TO_QUEUE!)
const NUM_ITERATIONS = parseInt(process.env.NUM_ITERATIONS!)

let totalNews = 0

async function runScraper(n: number) {
    const startTime = Date.now() // Start time for the entire process

    for (let i = 0; i < n; i++) {
        console.log(`\n--- Run ${i + 1} of ${n} ---`)
        try {
            const elements = await getMultipleUrlsToScrape(NUM_REQUESTS_TO_QUEUE)
            console.log(`Scraping ${elements.length} URLs`)

            await crawler.run(elements.map(element => element.url))

            // Save news as JSON after all runs are complete
            // saveNewsAsJson()

            // Save news to S3 after each run
            try {
                await newsToS3()
            } catch (err) {
                throw err 
            }

            try {
                await markUrlsAsScraped()
            } catch (err) {
                console.error('Error marking all as scraped:', err)
                throw err 
            }

            totalNews += getNewsSize()

            emptyResources()

        } catch (err) {
            console.error(`Error during run ${i + 1}:`, err)
            throw err // Stop the process if an error occurs
        }
    }



    logRunTime(startTime, getNewsSize()) // Log total runtime after all runs are complete
}

// Example usage: run the scraper 5 times
runScraper(NUM_ITERATIONS)
