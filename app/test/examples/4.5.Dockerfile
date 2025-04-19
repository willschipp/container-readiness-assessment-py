FROM microsoft/aspnet:4.5.2

# Install required packages
RUN apt-get update && \
    apt-get install -y libicu52 libcurl3

# Copy the application
WORKDIR /inetpub/wwwroot
COPY . .

# Expose port
EXPOSE 80

# Set entrypoint
ENTRYPOINT ["C:\\Windows\\System32\\inetsrv\\w3wp.exe"]