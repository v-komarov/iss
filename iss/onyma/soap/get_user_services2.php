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


        // Учетное имя
        function SiteName($client,$dmid) {
            $data=$client->o_mdb_api_func_get_sitename(array(pdmid=>(int)$dmid))->return;
            return $data;
        }


        // Название тарифного плана
        function TarifName($client,$tmid) {
            $data=$client->o_mdb_api_func_get_tm_name(array(ptmid=>(int)$tmid))->return;
            return $data;
        }


        // Название услуги
        function ServName($client,$pservid) {
            $res = $client->o_mdb_api_func_get_service_name(array(pservid=>(int)$pservid,plang=>1))->return;
            return $res;
        }


        // Название ресурса
        function ServiceName($client,$serviceid) {
            $data=$client->o_res_api_resources(array(id=>array(is=>(int)$serviceid)))->return;
            return $data->row->srvname;
        }


        $balans=$client->o_mdb_api_func_get_remainder_dog(array(pdogid=>$dogid,pdate=>$date))->return;
        print("balans:".$balans.";\n");

        //$data=$client->o_mdb_api_client_services(array(dogid=>array(is=>(int)$dogid),status=>array(is=>0)))->return;
        $data=$client->o_mdb_api_client_services(array(dogid=>array(is=>(int)$dogid)))->return;


        foreach ($data->row as &$row) {
            // Услуга
            $srv = ServiceName($client,$row->service);
            $start_date = $row->startdate;
            $login = $row->name;
            $sitename = SiteName($client,$row->dmid);
            $status = $row->status;

            // Для фингерпринта du
            if (substr($sitename,0,3) == "du.") {
                $r = $client->o_mdb_api_dog_serv_f(array(dmid=>array(is=>(int)$row->dmid)))->return;
                // Если значение servid одно
                if (isset($r->row->servid)) {
                    $tmidname = ServName($client,$r->row->servid);
                }
                // Если значений servid много
                else {
                        // Перебор и выбор названия
                        foreach ($r->row as &$row2) {

                          $tmidname = ServName($client,$row2->servid);

                        }
                }
            }
            else {
                $tmidname = TarifName($client,$row->tmid);
            }



            print("srv:".$srv.";start_date:".$start_date.";login:".$login.";tarif:".$tmidname.";sitename:".$sitename.";status:".$status.";\n");

        }


?>
