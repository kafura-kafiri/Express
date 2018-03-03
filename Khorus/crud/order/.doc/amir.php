public function sendOrderToZoodFoodExpress(Order $order , OrderExtraInfo $orderExtraInfo = null)
    {
        $uri = $this->container->get('request')->getHost();
        if(strpos($uri , 'local') === false) {
            $userMfr = null;
            $userOrderStatisticsModel = $this->em->getRepository('BodoFoodUserBundle:UserOrderStatistics');
            $userSegmentModel = $this->em->getRepository('BodoFoodUserBundle:UserSegment');

            $guzzle = $this->container->get('guzzle.client');
            $vendor = $order->getVendor();
            $user = $order->getCustomer();
            $userOrderStatisticsMFR = $userOrderStatisticsModel->findUserMFRByUserId($user->getId());
            if (!empty($userOrderStatisticsMFR)) {
                $mfr = $userSegmentModel->findProperSegmentOfUser($userOrderStatisticsMFR[0]['mfr']);
                if (!empty($mfr)) {
                    $userMfr = $mfr[0]['persianSegment'];
                }
            }
            $data = array();
            $source = array();
            $sourceLocation = array();
            $destination = array();
            $destinationLocation = array();
            $customer = array();
            $now = new \DateTime('+15 minutes');
            $riderPickupDateTime = $order->getRiderPickupDateTime();
            $timeToArrive = $now->getTimestamp();

            if ($riderPickupDateTime) {
                $timeToArrive = $riderPickupDateTime->getTimestamp();
            }
            $test = false;
            if ($vendor->getId() == 8555) {
                $test = true;
            }
            ///source part
            $source['title'] = $vendor->getTitle();
            $source['address'] = $vendor->getAddress();
            $sourceLocation['latitude'] = $vendor->getLatitude();
            $sourceLocation['longitude'] = $vendor->getLongitude();
            $source['location'] = $sourceLocation;
            $source['logo'] = $vendor->getLogoSource();
            $vendorPhones = $vendor->getCustomersPhone();
            $tempVendorPhones = array();
            if (strpos($vendorPhones, ',') !== false) {
                $tempVendorPhones = explode(',', $vendorPhones);
            } else {
                $tempVendorPhones = explode('-', $vendorPhones);
            }
            if (!empty($tempVendorPhones)) {
                $phone = $tempVendorPhones[0];
            } else {
                $phone = $vendorPhones;
            }
            if (strlen($phone) <= 8) {
                $phone = '021' . $phone;
            }
            $source['phone'] = preg_replace('/\s+/', '', trim($phone));

            ///destination part
            $address = !empty($order->getUserAddress()) ? $order->getUserAddress()->getAddress() : '';
            $destination['address'] = $address;
            //todo try to find solution for this, what is the lat and long of order delivery address
            $userAddress = $order->getUserAddress();
            $lat = $userAddress->getLatitude();
            $long = $userAddress->getLongitude();
            $destinationLocation['latitude'] = $lat ? $lat : -1;
            $destinationLocation['longitude'] = $long ? $long : -1;
            $destination['address'] = $address;
            $destination['location'] = $destinationLocation;

            ///customer part
//        $customer['phone'] = $user->getPlainCellphone();
            $customer['phone'] = $user->getPlainCellphone();
            $customer['name'] = $user->getFullName();
            $customer['customerId'] = $user->getId();
            $customer['rank'] = $userMfr;
            //order part
            $products = $order->getOrderProducts();
            $extraProducts = $order->getOrderExtraProducts();
            $productArray = array();
            /** @var OrderProduct $product */
            foreach ($products as $product) {
                $productArray[] = trim(str_replace('-', ' ', $product->getTitle()) . ' ' . str_replace('-', ' ', $product->getVariationTitle()) . '-' . $product->getQuantity() . '-' . $product->getPrice());
            }

            if ($extraProducts) {
                /** @var OrderExtraProduct $extraProduct */
                foreach ($extraProducts as $extraProduct) {
                    $productArray[] = $extraProduct->getTitle() . '-' . $extraProduct->getQuantity() . '-' . $extraProduct->getPrice();
                }
            }

            $comment = $order->getCustomerComment();
            if ($orderExtraInfo) {
                if (!empty($orderExtraInfo->getZoodfoodComment())) {
                    $comment = $orderExtraInfo->getZoodfoodComment();
                }
            }

            //code part
            $code = $this->hashIds->encode($order->getId());
            $data['preOrder'] = $order->getPreOrderDeliveryTime() != null;
            $data['source'] = $source;
            $data['destination'] = $destination;
            $data['customer'] = $customer;
            $data['order'] = implode('$', $productArray);
            $data['code'] = $code;
            $data['orderId'] = $order->getId();
            $data['time_to_arrive'] = $timeToArrive;
            $data['statusDate'] = $order->getStatusDate()->getTimestamp();
            $data['creationTime'] = $order->getCreatedAt()->getTimestamp();
            $data['description'] = $comment;
            $data['test'] = $test;
            $data['sourceCode'] = $vendor->getCode();
            $data['sourceId'] = $vendor->getId();
            $response = $guzzle->post('https://apiexpress.zoodfood.com/mobile/trip/create', array(
                    'verify' => false,
                    'headers' => array(
                        'User-Agent' => 'BodoFood',
                        'Content-Type' => 'application/json',
                        'Authorization' => 'Token e104f69eddbf657b40589dd59568ce26386be18f'

                    ),
                    'body' => json_encode($data)
                )
            );

            $result = $response->getBody()->getContents();

            if ($response->getStatusCode() == 200) {
                $inPlaceDeliveryOrderModel = $this->em->getRepository('BodoFoodOrderBundle:InPlaceDeliveryOrder');
                if ($inPlaceDeliveryOrderModel->getInPlaceOrderCountByOrderId($order->getId()) == 0) {
                    $inPlaceDeliveryOrder = new InPlaceDeliveryOrder();
                    $inPlaceDeliveryOrder->setCreatedAt(new \DateTime());
                    $inPlaceDeliveryOrder->setUpdatedAt(new \DateTime());
                    $inPlaceDeliveryOrder->setExpeditionType(OrderConstants::EXPEDITION_ZF_EXPRESS);
                    $inPlaceDeliveryOrder->setOrder($order);
                    $inPlaceDeliveryOrder->setStatus('REQUESTED');
                    try {
                        $this->em->persist($inPlaceDeliveryOrder);
                        $this->em->flush();
                    } catch (\Exception $ex) {

                    }
                }
                return true;
            } else {
                return false;
            }

        }


    }

