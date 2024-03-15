import Container from "../../components/common/Container";
import { useParams } from "react-router";
import { useGetSubscribeQuery } from "../../services/subscribesApi";
import Tag from "../../components/common/Tag";


export default function Subscription() {

    const { platform, id }: { platform: string, id: string } = useParams();
    const { data = [], isLoading } = useGetSubscribeQuery(`${platform} ${id}`);

    return (
        <Container>
            <div className="flex flex-col items-center">
                {!isLoading && data !== undefined ? (
                    <div className="flex flex-col items-start">
                        <img className="w-[346px] h-[400px] rounded-xl mb-8 object-cover" src={data.photoUrls[0]} alt="game image" />
                        <h1 className="text-header mb-2">{data.title}</h1>
                        <div className="flex items-center">
                            <h1 className="price-big">275 ₽</h1>
                        </div>
                        <h2 className="text-title text-[18px]">Издания</h2>
                    </div>
                ) : (<h1>Страница не найдена</h1>)
                }
            </div>
        </Container>
    )
}
