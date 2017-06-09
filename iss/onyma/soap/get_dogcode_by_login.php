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


        // Разбор строки.
        $logins = $argv[3];
        $arraylogins = explode("#",$logins);

        //
        $resultarray = array();

        // Поиск по каждому логину
        foreach ($arraylogins as &$login) {
            $result = $client->o_mdb_api_get_dog_get_dogid_by_prop(array(pprop=>(int)13865,pvalue=>(string)$login))->return;

            if (property_exists($result,'row')) {
		        if (is_array($result->row)) {
		            $dogid = end($result->row)->column_value;
		        }
		        else {
		            $dogid = $result->row->column_value;
		        }
                $data = $client->o_mdb_api_func_get_dogcode(array(pdogid=>(int)$dogid))->return;
                $resultarray0['login'] = $login;
                $resultarray0['dogid'] = $dogid;
                $resultarray0['dogcode'] = $data;

                $resultarray[] = $resultarray0;

            }
        }

        print json_encode($resultarray);


?>
