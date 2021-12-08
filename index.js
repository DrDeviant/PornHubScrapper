
async function start(){
    const pornhub = require('@justalk/pornhub-api');
    const url = 'https://www.pornhub.com/view_video.php?viewkey=ph61815c049428d';
    const video = await pornhub.page(url, ['title','pornstars','down_votes']);
    console.log(video)
}

start()
