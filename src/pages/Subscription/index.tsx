// import Container from "../../components/common/Container";
// import { useParams } from "react-router";
// import SubscriptionPeriodSelector from "../../components/common/SubscriptionPeriodSelect";
// import { useState } from "react";
// import SelectPublication from "../../components/common/SelectPublictaion";


// export default function Subscription() {

//     interface RouteParams {
//         [key: string]: string | undefined;
//         platform: string;
//         id: string;
//     }


//     const { platform, id } = useParams<RouteParams>();
//     const { data = [], isLoading } = platform === 'ps' ? useGetPsSubscribesQuery({}) : useGetEaSubscribesQuery({})


//     const [currentSubscription, setCurrentSubscription] = useState(data.find((sub) => sub.id === id))

//     const [selectedPeriod, setSelectedPeriod] = useState(1);

//     return (
//         <Container>
//             <div className="flex flex-col items-center">
//                 {!isLoading && currentSubscription !== undefined ? (
//                     <div className="flex flex-col items-start">
//                         <img className="w-[346px] h-[400px] rounded-xl mb-8 object-cover" src={currentSubscription.photoUrls[0]} alt="game image" />
//                         <h1 className="text-header mb-2">{currentSubscription.title}</h1>
//                         <div className="flex items-center">
//                             <h1 className="price-big">275 ₽</h1>
//                         </div>
//                         <div className="flex flex-col mt-[18px]">
//                             <h2 className="text-title text-[18px] mb-[25px]">Издания</h2>
//                             <SubscriptionPeriodSelector onChange={setSelectedPeriod} selected={selectedPeriod} />
//                         </div>
//                     </div>
//                 ) : (<h1>Страница не найдена</h1>)
//                 }
//             </div>
//         </Container>
//     )
// }
