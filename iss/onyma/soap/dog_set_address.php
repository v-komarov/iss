<?php

error_reporting(1);


$username=$argv[1];
$password=$argv[2];


$date = date("Y-m-d\T00:00:00.000\Z", time());


    class AuthHeader
    {
        var $skey;//string
        var $operid;//string
        var $username;//string
        var $password;//string

        function __construct($LoginResponse)
            {
                $this->skey  = $LoginResponse->skey;
                $this->operid = $LoginResponse->operid;
                $this->username    = $LoginResponse->username;
                $this->password    = $LoginResponse->password;
            }
    }



    $soapParams=array(
	    'trace' => 1,
            'exceptions' => 1,
            'stream_context'  => stream_context_create(
                        [
                            'ssl' => [
                                'verify_peer'      => false,
                                'verify_peer_name' => false,
                                'allow_self_signed' => true]
                        ])
    );


    $wsdl="iss/onyma/soap/service.htms";

    $client = new SoapClient($wsdl,$soapParams);
    use_soap_error_handler(false);

        $LoginResponse=$client->onyma_api_open_session(array(username=>$username, password=>$password));
        $LoginResponse->username=$username;
        $LoginResponse->password=$password;

	    $ns='http://www.onyma.ru/services/OnymaApi/heads/';
        $AuthHeader = new AuthHeader($LoginResponse);
        $header =  new SoapHeader($ns, "credentials", $AuthHeader, false);
        $client->__setSoapHeaders(array($header));

        $dogid = 1*$argv[3];
        $city = str_replace("#"," ",$argv[4]); // город
        $street = str_replace("#"," ",$argv[5]); // улица
        $house = str_replace("#"," ",$argv[6]); // дом
        $room = str_replace("#"," ",$argv[7]); // квартира

        // Адрес

        $data=$client->o_mdb_api_change_dog_add_dog_attrib_insert(array(pdogid=>$dogid,pattrid=>289,pval=>$room,pattridup=>292))->return;
        $data=$client->o_mdb_api_change_dog_add_dog_attrib_insert(array(pdogid=>$dogid,pattrid=>287,pval=>$house,pattridup=>292))->return;
        $data=$client->o_mdb_api_change_dog_add_dog_attrib_insert(array(pdogid=>$dogid,pattrid=>286,pval=>$street,pattridup=>292))->return;
        $data=$client->o_mdb_api_change_dog_add_dog_attrib_insert(array(pdogid=>$dogid,pattrid=>284,pval=>$city,pattridup=>292))->return;
        $data=$client->o_mdb_api_change_dog_add_dog_attrib_insert(array(pdogid=>$dogid,pattrid=>292,pval=>$city." ".$street." ".$house." ".$room))->return;


        print_r($data);


?>
