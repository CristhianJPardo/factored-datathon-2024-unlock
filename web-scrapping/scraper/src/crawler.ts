import { CheerioCrawler } from 'crawlee'
import { IUrlElement, addNew, searchInBlockedStack } from './helpers.js'

const MAX_CONCURRENCY = parseInt(process.env.MAX_CONCURRENCY!)
const MIN_CONCURRENCY = parseInt(process.env.MIN_CONCURRENCY!)
const NAVIGATION_TIMEOUT_SECS = parseInt(process.env.NAVIGATION_TIMEOUT_SECS!)
const MAX_REQUEST_RETRIES = parseInt(process.env.MAX_REQUEST_RETRIES!)

function getTitle($: any): string | null {
    // Attempt to get the title using different common selectors
    const title = $('meta[property="og:title"]').attr('content') || // Open Graph title
        $('meta[name="twitter:title"]').attr('content') || // Twitter card title
        $('title').text() || // Standard title tag
        $('h1').first().text() // First H1 tag as a fallback

    return title ? title.trim() : null
}

function getContent($: any): string {
    // Attempt to get the main content using common selectors
    let content = $('article').text() || // Common article tag
        $('[role="main"]').text() || // Main role as fallback
        $('main').text() || // Main tag
        $('div.content').text() || // Div with class 'content'
        $('p').map((_i: any, el: any) => $(el).text()).get().join('\n') // Fallback to all paragraphs

    // Clean up the content by trimming and removing excessive white space
    content = content.replace(/\s\s+/g, ' ').trim()

    // Remove JavaScript, URLs, and other unwanted content
    content = content.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '') // Remove script tags
        .replace(/(new\sImage\(\)|cnx.cmd.push|document\.write)/gi, '') // Remove common JS patterns
        .replace(/https?:\/\/[^\s]+/g, '') // Remove URLs
        .replace(/['"]https?:\/\/[^'"]+['"]/g, '') // Remove URL-like strings
        .replace(/(\{.*?\})|(\[.*?\])|(\(.*?\))/g, '') // Remove content inside {}, [], or ()
        .replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, '') // Remove style tags
        .replace(/<!--[\s\S]*?-->/g, '') // Remove HTML comments
        .replace(/(\.\w+[_\-\w\d]*)+/g, '') // Remove CSS class names that might appear as text

    // Additional cleanup for specific patterns
    content = content.replace(/['"]?var\s[\w\d]+\s?=\s?[^;]+;/g, '') // Remove JS variable declarations
        .replace(/^\s*[\r\n]/gm, '') // Remove empty lines
        .replace(/^\s+|\s+$/gm, '') // Remove leading/trailing whitespace in each line
        .replace(/^\s*$/gm, '') // Remove lines that are just whitespace

    return content.trim()
}



export const crawler = new CheerioCrawler({
    async requestHandler({ request, $ }) {
        console.log(`Scraping ${request.url}`)

        const title = getTitle($)

        // Check if the title indicates an error or unwanted page
        const errorIndicators = ['404', 'Not Found', 'Error', 'Captcha', 'Forbidden', 'Access Denied']
        const titleLower = title?.toLowerCase() || '' // Convert title to lowercase for case-insensitive comparison

        const isErrorPage = errorIndicators.some(indicator => titleLower.includes(indicator.toLowerCase()))

        if (isErrorPage) {
            console.log(`Skipping ${request.url} - detected error page or captcha`)
            return // Skip saving if an error page is detected
        }

        const content = getContent($)

        if (!content) {
            console.log(`Skipping ${request.url} - no content found`)
            return // Skip saving if no content is found
        }

        const remainingData: IUrlElement = searchInBlockedStack(request.url)

        addNew({
            title: title || 'untitled',
            content: content,
            url: remainingData.url,
            md5_id: remainingData.md5_id
        })

        console.log(`Added ${request.url} to news array`)
    },
    maxConcurrency: MAX_CONCURRENCY,
    minConcurrency: MIN_CONCURRENCY,
    navigationTimeoutSecs: NAVIGATION_TIMEOUT_SECS,
    maxRequestRetries: MAX_REQUEST_RETRIES,
})