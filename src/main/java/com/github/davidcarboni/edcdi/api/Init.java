package com.github.davidcarboni.edcdi.api;

import com.github.davidcarboni.cryptolite.Keys;
import com.github.davidcarboni.restolino.framework.Startup;

import java.security.KeyPair;

/**
 * Created by david on 16/02/16.
 */
public class Init  extends Startup {

    public static KeyPair keyPair;
    @Override
    public void init() {
        keyPair = Keys.newKeyPair();
    }
}
