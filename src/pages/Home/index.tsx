import Donation from "../../components/Home/Donation";
import HeaderSlider from "../../components/Home/HeaderSlider";
import Leaders from "../../components/Home/Leaders";
import NewGames from "../../components/Home/NewGames";
import Subscribes from "../../components/Home/Subscribes";
import Container from "../../components/common/Container";
import Navigation from "../../components/common/Navigation";

export default function Home() {
    return (
        <Container>
            <Navigation />
            <HeaderSlider />
            <NewGames />
            <Subscribes />
            <Leaders />
            <Donation />
        </Container>
    )
}
