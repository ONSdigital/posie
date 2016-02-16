package com.github.davidcarboni.edcdi.api;

import com.github.davidcarboni.cryptolite.Random;
import com.github.davidcarboni.restolino.helpers.Path;
import org.apache.commons.io.IOUtils;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import java.io.IOException;
import java.io.InputStream;

/**
 * Gets an encrypted file.
 */
public class Result {

    @POST
    public String receive(HttpServletRequest request, HttpServletResponse response) {
        System.out.println("Received a result! Did nothing with it though.");
    }
}
