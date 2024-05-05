import { useEffect } from "react";
import Donation from "../../components/Home/Donation";
import HeaderSlider from "../../components/Home/HeaderSlider";
import Leaders from "../../components/Home/Leaders";
import NewGames from "../../components/Home/NewGames";
import Other from "../../components/Home/Other";
import Subscribes from "../../components/Home/Subscribes";
import Container from "../../components/common/Container";
import Navigation from "../../components/common/Navigation";
import { useGetCategoryProductsQuery } from "../../services/productsApi";
import { SectionType } from "../../types/SectionType";
import cookie from 'cookiejs';

export default function Home() {

    const { data = [] } = useGetCategoryProductsQuery({})

    function getTokenFromUrl(url) {
        const tokenRegex = /token=([^&#]+)/;
        const match = url.match(tokenRegex);

        if (match && match[1]) {
            return match[1];
        } else {
            return null;
        }
    }

    console.log(getTokenFromUrl('https://chatlabs.site/aokibot/frontend/?token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZWxlZ3JhbV9pZCI6NjQ5OTM5MTM4LCJ0b2tlbl9leHBpcmF0b24iOiIyMDI0LTA1LTA1VDIzOjIyOjU2LjY1NDI5MiIsInRva2VuX3NlZWQiOiI2OGM0NzJhNTVjNjQ0OTk0OGE1NGE2MWMyYzg3ZmJhNCJ9.nWe3p3VSALuP3YHAEiu6y85P3fnZy86foOAGPtNhRYw3UncnJswpRBsQrSOK_w2oLXrWpvcgMbE34OYh-TLTs8XqBq4hCP1T3yDFz8ROBjGGHFhasaNYEShufhj2ySl_cZ3GqkrbLIa-nwv4qhi8JsC84rXeuVRYXXzFHHfPeSndhVLObpCqkzRS_75Xo4m9VhyV6OL7S1B22aEWomDnxAlTcoVG8A98_9t21UhSWxGq2joGLMPUWtytqriA7EUl_HP55FdqXAy2qOAJ4pR55xvA8V3WwyN8iLXh4wt8beAdw4hOIUwiv60yOlcTgIBjJOPwxDjAw7UTiV2COiezxA#tgWebAppData=query_id%3DAAHCSL0mAAAAAMJIvSY66XWf%26user%3D%257B%2522id%2522%253A649939138%252C%2522first_name%2522%253A%2522Saul%2520Goodman%2522%252C%2522last_name%2522%253A%2522%2522%252C%2522username%2522%253A%2522Tw1nklee%2522%252C%2522language_code%2522%253A%2522ru%2522%252C%2522allows_write_to_pm%2522%253Atrue%257D%26auth_date%3D1714933638%26hash%3Db5f7e0f95f77352384e2c863349f1e2e0128768d370c3bff307c812d07aaa92d&tgWebAppVersion=7.2&tgWebAppPlatform=weba&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23212121%22%2C%22text_color%22%3A%22%23ffffff%22%2C%22hint_color%22%3A%22%23aaaaaa%22%2C%22link_color%22%3A%22%238774e1%22%2C%22button_color%22%3A%22%238774e1%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22secondary_bg_color%22%3A%22%230f0f0f%22%2C%22header_bg_color%22%3A%22%23212121%22%2C%22accent_text_color%22%3A%22%238774e1%22%2C%22section_bg_color%22%3A%22%23212121%22%2C%22section_header_text_color%22%3A%22%23aaaaaa%22%2C%22subtitle_text_color%22%3A%22%23aaaaaa%22%2C%22destructive_text_color%22%3A%22%23e53935%22%7D'))

    useEffect(() => {
        const newToken = getTokenFromUrl(window.location.href);
        if (newToken !== null) {
            cookie.set('token', newToken);
        }
    }, [])


    return (
        <Container>
            <Navigation />
            <HeaderSlider data={data.find((item: SectionType) => item.tag === "offers")} />
            <NewGames data={data.find((item: SectionType) => item.tag === "new")} />
            <Subscribes psSubs={data.find((item: SectionType) => item.tag === "psPlus")} eaSubs={data.find((item: SectionType) => item.tag === "eaPlay")} />
            <Leaders data={data.find((item: SectionType) => item.tag === "leaders")} />
            <Donation data={data.find((item: SectionType) => item.tag === "donation")} />
            <Other data={data.filter((item: SectionType) => item.tag === "other")} />
        </Container>
    )
}
