import { readFileSync } from "fs"
import { existsSync, mkdirSync, writeFileSync } from "fs"
import short from "short-uuid"
import path from "path"
import AWS from 'aws-sdk'

const sqsBatchSize = parseInt(process.env.SQS_BATCH_SIZE!)
const BASE_URL = process.env.BASE_URL!

const blockedStack: IUrlElement[] = []

export interface INew {
    title: string
    content: string
    url: string
    md5_id: string
    // receipt_handle: string
}

const news: INew[] = []

export const getNewsSize = () => {
    return news.length
}

export const addNew = (newElement: INew) => {
    news.push(newElement)
}


export const addToBlockedStack = (elements: IUrlElement[]) => {
    elements.forEach(element => {
        blockedStack.push(element)
    })
}

export const searchInBlockedStack = (url: string): IUrlElement => {
    const index = blockedStack.findIndex(element => element.url === url)
    if (index >= 0) {
        return blockedStack[index]
    }
    throw new Error("Element not found in blocked stack")
}

export const emptyBlockedStack = () => {
    blockedStack.length = 0
}

export const emptyNews = () => {
    news.length = 0
}

export const emptyResources = () => {
    emptyBlockedStack()
    emptyNews()
}

export const saveNewsAsJson = () => {
    const extractionDir = 'extraction'
    // Generate a short UUID for the filename
    const translator = short()
    const fileName = `${translator.new()}.json`

    // Ensure the extraction directory exists
    if (!existsSync(extractionDir)) {
        mkdirSync(extractionDir, { recursive: true })
    }

    // Define the full file path
    const filePath = path.join(extractionDir, fileName)

    // Write the news array to the JSON file
    writeFileSync(filePath, JSON.stringify(news, null, 2), 'utf-8')

    console.log(`News saved to ${filePath}`)
}

// save json file in s3 bucket function
export const newsToS3 = async () => {
    AWS.config.update({
        region: process.env.AWS_REGION,
        accessKeyId: process.env.AWS_ACCESS_KEY_ID,
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
    })
    const s3 = new AWS.S3()

    const params = {
        Bucket: process.env.BUCKET_NAME,
        Key: `scraped/${short().new()}.json`,
        Body: JSON.stringify(news, null, 2),
    }

    try {
        const data = await s3.upload(params as any).promise()
        console.log(`File uploaded successfully. ${data.Location}`)
    } catch (err) {
        console.error(`Error uploading file: ${err}`)
    }
}



export const loadSourceUrls = (trunc = 0): string[] => {
    const fileName = 'source_urls.json'
    const data = readFileSync(fileName, 'utf-8')
    let sourceUrls: string[] = JSON.parse(data)
    if (trunc) {
        sourceUrls = sourceUrls.slice(0, trunc)
    }
    return sourceUrls
}
export interface IUrlElement {
    url: string
    md5_id: string
    receipt_handle: string
}

const baseUrl = BASE_URL

export const getUrlToScrape = (): Promise<IUrlElement[]> =>
    new Promise((resolve, reject) => {
        const url = `${baseUrl}/get_url?batch_size=${sqsBatchSize}`
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Unable to get url with status: " + response.status)
                }
                return response.json()
            })
            .then(data => { resolve(data) })
            .catch(reject)
    })

export const getMultipleUrlsToScrape = async (count = 10): Promise<IUrlElement[]> => {
    const promises = []
    for (let i = 0; i < count; i++) {
        promises.push(getUrlToScrape())
    }
    const elements = await Promise.all(promises)
    const elementsFlat = elements.flat()
    addToBlockedStack(elementsFlat)
    return elementsFlat
}


export const markUrlAsScraped = (url: string): Promise<void> =>
    new Promise((resolve, reject) => {
        const fetchUrl = `${baseUrl}/post_url/`

        const request = searchInBlockedStack(url)
        fetch(fetchUrl, {
            method: 'POST',
            body: JSON.stringify([{ receipt_handle: request.receipt_handle }]),
            headers: { 'Content-Type': 'application/json' }
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Unable to mark as scraped with status: " + response.status)
                }
                // increaseTotalScraped()
                resolve()
            })
            .catch(reject)
    })


export const logRunTime = (startTime: number, newsSize: number): void => {
    const timeTaken = Date.now() - startTime
    const days = Math.floor(timeTaken / (1000 * 60 * 60 * 24))
    const hours = Math.floor((timeTaken % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
    const minutes = Math.floor((timeTaken % (1000 * 60 * 60)) / (1000 * 60))
    const seconds = Math.floor((timeTaken % (1000 * 60)) / 1000)
    console.log(`Time taken: ${days}d ${hours}h ${minutes}m ${seconds}s | Total news: ${newsSize}`)
}

export const sanitizeTitle = (title: string): string => {
    return title.replace(/[\/\\?%*:|"<>]/g, '_').trim() + '.json'
}